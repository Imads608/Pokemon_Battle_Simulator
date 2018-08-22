import random

def determineFunctionCodeEffects(functionCode, internalMove, action, attackerPokemon, opponentPokemon, movesDatabase, functionCodesMap, battleFieldObject):
    description, effect = functionCodesMap.get(functionCode)
    identifierNum, fullName, functionCode, basePower, typeMove, damageCategory, accuracy, totalPP, description, addEffect, targetCode, priority, flag = movesDatabase.get(internalMove)
    randNumber = random.randint(1, 100)
    randNumber2 = random.randint(1, 100)
    randNumber3 = random.randint(1, 3)

    if (description == "No effects and pseudo-moves"):
        if (functionCode == "1"):
            action.setBattleMessage("Nothing Happened")

        elif (functionCode == "2"):
            recoilDamage = int(attackerPokemon.finalStatList[0] * (1 / 4))
            action.setRecoil(recoilDamage)

    elif (description == "Status Problems"):
        if (functionCode == "3"):
            if (randNumber <= int(accuracy)):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 4))
                action.setMessage(opponentPokemon.name + " fell asleep")
            else:
                action.setMessage("But it missed")

        elif (functionCode == "4"):
            if (
                    "Uproar" not in battleFieldObject.fieldHazards and opponentPokemon.statusConditionIndex != 8 and opponentPokemon.statusConditionIndex != 4):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 8))
                action.setMessage(opponentPokemon.name + " yawned")
            else:
                action.setMessage("But it failed")

        elif (functionCode == "5"):
            if (damageCategory == "Status" and randNumber > int(accuracy)):
                action.setMessage("But it missed")
            elif (damageCategory == "Status" and opponentPokemon.statusConditionIndex != 0):
                action.setMessage("But it failed")
            elif (((damageCategory == "Status" and randNumber <= int(accuracy)) or (
                    damageCategory != "Status" and randNumber <= int(
                    addEffect))) and opponentPokemon.statusConditionIndex == 0):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 1))
                action.setMessage(opponentPokemon.name + " is poisoned")

        elif (functionCode == "6"):
            if (internalMove == "TOXIC" and randNumber > int(accuracy)):
                action.setMessage("But it missed")
            elif (internalMove == "TOXIC" and opponentPokemon.statusConditionIndex != 0):
                action.setMessage("But it failed")
            elif (((internalMove == "TOXIC" and randNumber <= int(accuracy)) or (
                    randNumber <= int(addEffect))) and opponentPokemon.statusConditionIndex == 0):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 2))
                action.setMessage(opponentPokemon.name + " is badly poisoned")

        elif (functionCode == "7" or functionCode == "8"):
            if (internalMove == "THUNDERWAVE" and "GROUND" in opponentPokemon.types):
                action.setMessage("But it failed")
            elif (internalMove == "BOLTSTRIKE"):
                _, _, _, bPower, _, _, _, _, _, _, _, _, _ = movesDatabase.get("FUSIONFLARE")
                movePowered = ("FUSIONFLARE", bPower * 2)
                if (randNumber <= int(addEffect) and opponentPokemon.statusConditionIndex == 0):
                    action.moveObject.setStatusCondition((opponentPokemon.playerNum, 3))
                    action.setMessage(opponentPokemon.name + " is paralyzed")
            elif (damageCategory == "Status" and randNumber > int(accuracy)):
                action.setMessage("But it missed")
            elif (damageCategory == "Status" and opponentPokemon.statusConditionIndex != 0):
                action.setMessage("But it failed")
            elif ((damageCategory == "Status" or randNumber <= int(
                    addEffect)) and opponentPokemon.statusConditionIndex == 0):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 3))
                action.setMessage(opponentPokemon.name + " is paralyzed")

        elif (functionCode == "9"):
            if (randNumber <= 10):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 3))
                action.setMessage(opponentPokemon.name + " is paralyzed")
            if (randNumber2 <= 10):
                action.moveObject.setFlinchValid()
                action.setMessage(opponentPokemon.name + " flinched")

        elif (functionCode == "00A"):
            if (internalMove == "BLUEFLARE"):
                _, _, _, bPower, _, _, _, _, _, _, _, _, _ = movesDatabase.get("FUSIONBOLT")
                movePowered = ("FUSIONFLARE", bPower * 2)
                if (randNumber <= int(addEffect) and opponentPokemon.statusConditionIndex == 0):
                    action.moveObject.setStatusCondition((opponentPokemon.playerNum, 6))
                    action.setMessage(opponentPokemon.name + " is burned")
            elif (damageCategory == "Status" and randNumber > int(accuracy)):
                action.setMessage("But it missed")
            elif (damageCategory == "Status" and opponentPokemon.statusConditionIndex != 0):
                action.setMessage("But it failed")
            elif ((damageCategory == "Status" or randNumber <= int(
                    addEffect)) and opponentPokemon.statusConditionIndex == 0):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 6))
                action.setMessage(opponentPokemon.name + " is burned")

        elif (functionCode == "00B"):
            if (randNumber <= 10):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 6))
                action.setMessage(opponentPokemon.name + " is burned")
            if (randNumber2 <= 10):
                action.moveObject.setFlinchValid()
                action.setMessage(opponentPokemon.name + " flinched")

        elif (functionCode == "00C" or functionCode == "00D"):
            if (randNumber <= int(addEffect) and opponentPokemon.statusConditionIndex == 0):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 5))
                action.setMessage(opponentPokemon.name + " is frozen")

        elif (functionCode == "00E"):
            if (randNumber <= 10):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 5))
                action.setMessage(opponentPokemon.name + " is frozen")
            if (randNumber2 <= 10):
                action.moveObject.setFlinchValid()
                action.setMessage(opponentPokemon.name + " flinched")

        elif (functionCode == "00F" or functionCode == "10" or functionCode == "11" or functionCode == "12"):
            if (randNumber <= int(addEffect)):
                action.moveObject.setFlinchValid()

        elif (functionCode == "13"):
            if (damageCategory == "Status" and randNumber > int(accuracy)):
                action.setMessage("But it missed")
            elif (damageCategory == "Status" or randNumber <= int(addEffect)):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 9))
                action.setMessage(opponentPokemon.name + " became confused")

        elif (functionCode == "14"):
            pass

        elif (functionCode == "15"):
            if (randNumber <= int(addEffect)):
                action.moveObject.setStatusCondition((opponentPokemon.playerNum, 9))
                action.setMessage(opponentPokemon.name + " became confused")

        elif (functionCode == "16"):
            if (randNumber <= int(addEffect)):
                if (randNumber3 == 1 and opponentPokemon.statusConditionIndex == 0):
                    action.moveObject.setStatusCondition((opponentPokemon.playerNum, 6))
                    action.setMessage(opponentPokemon.name + " is burned")
                elif (randNumber3 == 2 and opponentPokemon.statusConditionIndex == 0):
                    action.moveObject.setStatusCondition((opponentPokemon.playerNum, 5))
                    action.setMessage(opponentPokemon.name + " is frozen")
                elif (randNumber3 == 3 and opponentPokemon.statusConditionIndex == 0):
                    action.moveObject.setStatusCondition((opponentPokemon.playerNum, 3))
                    action.setMessage(opponentPokemon.name + " became paralyzed")

        elif (functionCode == "17"):
            pass