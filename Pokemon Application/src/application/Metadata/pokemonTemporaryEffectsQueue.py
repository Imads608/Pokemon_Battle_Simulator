class PokemonTemporaryEffectsNode(object):
    def __init__(self, key, values):
        if (key == None):
            self.mapEffects = None
        else:
            self.mapEffects = {key:values}
        self.next = None

class PokemonTemporaryEffectsQueue(object):
    def __init__(self):
        self.queue = None
        self.size = 0
    

    def enQueue(self, key, values, turns):
        if (self.isEmpty() == True):
            newNode = PokemonTemporaryEffectsNode(key, values)
            self.queue = newNode
            self.size += 1
            return (True, None)
        elif (self.queue.mapEffects.get(key) != None and key not in ["move block"]):
            return (False, "Already Exists")
        elif (key in ["move block"]):
            localVals = self.queue.mapEffects.get(key)
            moveInternalName = list(values[1].keys())[0]
            metadata = values[1].get(moveInternalName)
            if (localVals[1].get(moveInternalName) != None):
                return (False, "Already Exists")
            localVals[1].update({moveInternalName:metadata})
            self.queue.mapEffects.update({key:localVals})
        elif (turns == -1):
            self.queue.mapEffects.update({key:values})
            return (True, None)
        self.insertEffect(key, values, turns)
        return (True, None)

    def deQueue(self):
        if (self.isEmpty() == True):
            return None
        dequeuedEffects = self.queue.mapEffects
        self.queue = self.queue.next
        self.size -= 1
        self.checkPersistentEffects(dequeuedEffects)
        return dequeuedEffects

    def seek(self):
        if (self.isEmpty() == True):
            return None
        seekedMap = self.queue.mapEffects
        return seekedMap

    def checkPersistentEffects(self, mapEffects):
        persistentEffects = {}
        for key in mapEffects:
            values = mapEffects.get(key)
            if (values[0] == -1 and self.queue != None):
                self.queue.mapEffects.update({key:values})
        if (self.queue == None):
            self.queue = PokemonTemporaryEffectsNode(None, None)
            self.queue.mapEffects = persistentEffects
            self.size += 1

    def insertEffect(self, key, values, turns):
        currNode = self.queue
        i = 0
        while (i < turns):
            if (currNode.next != None):
                #if (key in ["moves blocked"])
                currNode.mapEffects.update({key:values})
                currNode = currNode.next
            else:
                newNode = PokemonTemporaryEffectsNode(key, values)
                currNode.next = newNode
                currNode = newNode
            i += 1
        if (turns > self.size):
            self.size = turns
        return

    def isEmpty(self):
        if (self.queue == None):
            return True
        return False