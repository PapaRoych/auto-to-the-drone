from mavsdk import System
from time import sleep 
import asyncio



class DroneSystem0():
    
    def __init__(self):
        self.drone = System()
        self.state = None 
        
    
    
    async def drone_connect(self):
        await self.drone.connect(system_address="udp://:14540")
        print("Проводится подключение к дрону...")
        await asyncio.sleep(1) 
        async for self.state in self.drone.core.connection_state():
            if self.state.is_connected:
                print("Проводится проверка подключения, дождитесь её окончания")
                await asyncio.sleep(1)
                print("Подключение прошло успешно, дрон готов к запуску")
                break
            else:
                print("Ошибка подключения")
   
    
    async def drone_arming(self):
        if self.state.is_connected:
            print("Производится запуск моторов...")
            await self.drone.action.arm()
            await asyncio.sleep(1)
            print("Запуск произведён успешно...")
        else:
            print("Ошибка соединения...")
    
    
    async def drone_disarm(self):
        if self.drone.telemetry.armed()or self.state.is_connected:
            print("Производится остановка дрона...")
            await asyncio.sleep(1)
            await self.drone.action.disarm()
            await asyncio.sleep(1)
            print("Дрон произвёл остановку моторов")
        else: 
            print("Ошибка,ты чё еблан, моторы даже не запущены...Пиииздееец")
        

    async def drone_takeoff(self):
        if self.drone.telemetry.armed() or self.state.is_connected:
            print("Производится взлёт дрона...")
            await self.drone.action.takeoff()
            await asyncio.sleep(1)
            await asyncio.sleep(1)
            print("Взлёт произведён...")
        else:
            print("Ошибка, проверьте был ли произведен запуск моторов...")
    
    async def drone_land(self):
        if self.drone.telemetry.armed() or self.state.is_connected:
            print("Производится посадка...")
            await self.drone.action.land()
            await asyncio.sleep(1)
            await asyncio.sleep(1)
            print ("Посадка была произведена...")
        else:
            print("Ошибка, долбаеб ты даже не взлетел...")
    
        

            
if __name__ == "__main__":
    
    app = DroneSystem0()
    asyncio.get_event_loop().run_until_complete(app.drone_connect())


        