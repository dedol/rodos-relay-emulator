from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Relay():
    id: int
    state: str = 'OFF'
    timer: Optional[int] = None


class Rodos():
    def __init__(self, socketio, scheduler, channels=2) -> None:
        self.socketio = socketio
        self.scheduler = scheduler
        self.states = [Relay(id=x) for x in range(channels)]


    def get_relay(self, id: int) -> Relay:
        relay = next(filter(lambda r: r.id == id, self.states))
        self.cancel_timer(relay)
        return relay


    def cancel_timer(self, relay: Relay) -> None:
        if relay.timer:
            jobs = self.scheduler.get_jobs()
            job_id = f'{relay.id}_{relay.timer}'
            if any(filter(lambda job: job.id == job_id, jobs)):
                self.scheduler.remove_job(job_id)
            relay.timer = None


    def get_states(self) -> List[Relay]:
        return self.states
    

    def get_states_xml(self) -> str:
        response = ['<response>']
        for relay in self.states:
            state = '1' if relay.state == 'ON' else '0'
            string = f'<rl{relay.id}string>{state}</rl{relay.id}string>'
            response.append(string)
        response.append('</response>')
        return '\n'.join(r for r in response)


    def set_state(self, id: int, state: str) -> None:
        relay = self.get_relay(id)
        relay.state = state
        self.socketio.emit('update', data=asdict(relay))

    
    def set_timer(self, id: int, seconds: int) -> None:
        relay = self.get_relay(id)
        relay.state = 'ON'
        relay.timer = int(datetime.now().timestamp() * 1000) + seconds * 1000

        self.scheduler.add_job(
            f'{id}_{relay.timer}',
            self.set_state,
            args=[id, 'OFF'],
            trigger='date',
            run_date=datetime.fromtimestamp(int(relay.timer / 1000))
        )
        self.socketio.emit('update', data=asdict(relay))