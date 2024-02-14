from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId


class CompetitiveBot(BotAI):
    NAME: str = "DragonBot"
    """This bot's name"""

    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")
        
        
    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        """
        """
        print(f"this is my bot in iteration {iteration}") #print iteration
        """
        await self.distribute_workers() #puts idle workers to work

        nexus = self.townhalls.ready.random

        # if a random nexus is not idle and not chrono boosting, chrono boost it
        #if not nexus.is_idle and not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
         #   if self.can_afford(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus):
          #      nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)
           #     print("Chrono Boosted")


        # Build a pylon if we are low on supply
        if self.supply_left < 2 and self.already_pending(UnitTypeId.PYLON) == 0:
            if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)
            return
        
        for loop_nexus in self.workers:
            nexus_list = self.structures(UnitTypeId.NEXUS).ready.idle  # Get list of idle nexuses
            if self.can_afford(UnitTypeId.PROBE) and self.workers.amount < 16 and nexus_list.exists: # Need to look at after expanding, only works for 1 nexus
                self.townhalls.ready.random.train(UnitTypeId.PROBE)
        
                # Add break statement here if you only want to train one
            else:
                # Can't afford probes anymore
                break
            
        

        if self.can_afford(UnitTypeId.GATEWAY) and self.structures(UnitTypeId.GATEWAY).amount < 2:
            pylon = self.structures(UnitTypeId.PYLON).ready
            if pylon.exists:
                if self.can_afford(UnitTypeId.GATEWAY):
                    await self.build(UnitTypeId.GATEWAY, near=pylon.random)
                    print("Gateway built")

        # Check for ready gateways and build zealots
        zealots = self.units(UnitTypeId.ZEALOT)
        gateways = self.structures(UnitTypeId.GATEWAY).ready.idle
        if gateways.exists and self.can_afford(UnitTypeId.ZEALOT):
            for gateway in gateways:
                if len(zealots) < 12:
                    gateway.train(UnitTypeId.ZEALOT)
                    
                
        if len(zealots) == 12:
            for zealot in zealots:
                zealot.attack(self.enemy_start_locations[0])

        
            
    
    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
