class LogicGate:

    def __init__(self,n):
        self.label = n
        self.output = None

    def getLabel(self):
        return self.label

    def getOutput(self):
            self.output = self.performGateLogic()
            return self.output
    
class BinaryGate(LogicGate):

    def __init__(self,n):
        LogicGate.__init__(self,n)

        self.pinA = None
        self.pinB = None

    def getPinA(self):
        if self.pinA == None:    
            return int(input("Enter Pin A input for gate "+ self.getLabel()+"-->"))
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB == None:    
            return int(input("Enter Pin B input for gate "+ self.getLabel()+"-->"))
        else:
            return self.pinB.getFrom().getOutput()
    
    def setNextPin(self,source):
        if self.pinA == None:
            self.pinA = source
        else:
            if self.pinB == None:
             self.pinB = source
            else:
                raise RuntimeError("Error: NO EMPTY PINS")
    
class UnaryGate(LogicGate):

    def __init__(self,n):
        LogicGate.__init__(self,n)

        self.pin = None

    def getPin(self):
        if self.pin == None:    
            return int(input("Enter Pin input for gate "+ self.getLabel()+"-->"))
        else:
            return self.pin.getFrom().getOutput()
        
    def setNextPin(self,source):
        if self.pin == None:
            self.pin = source
        else:
            print("Cannot Connect: NO EMPTY PINS on this gate")      

class Power(UnaryGate):
    def __init__(self,n):
        LogicGate.__init__(self,n)
    
    def performGateLogic(self):
        return 1
    
class Ground(UnaryGate):
    def __init__(self,n):
        LogicGate.__init__(self,n)
    
    def performGateLogic(self):
        return 0

class Switch(UnaryGate):
    def __init__(self, n):
        super(Switch,self).__init__(n)
    
    def performGateLogic(self):
            return self.getPin()

    
class AndGate(BinaryGate):

    def __init__(self,n):
        super(AndGate,self).__init__(n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 1
        else:
            return 0

class OrGate(BinaryGate):

    def __init__(self,n):
        super(OrGate,self).__init__(n)
    
    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 or b==1:
            return 1
        else:
            return 0

class NotGate(UnaryGate):
    
    def __init__(self,n):
        super(NotGate,self).__init__(n)

    def performGateLogic(self):
        if self.getPin() == 0:
            return 1
        else:
            return 0
        
class Connector:
    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate
        tgate.setNextPin(self)

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate
    
class NorGate(BinaryGate):

    def __init__(self,n):
        super(NorGate,self).__init__(n)
    
    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==0 and b==0:
            return 1
        else:
            return 0
        
class NandGate(BinaryGate):

    def __init__(self,n):
        super(NandGate,self).__init__(n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 0
        else:
            return 1
        
class XorGate(BinaryGate):

    def __init__(self,n):
        super(XorGate,self).__init__(n)
    
    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==0:
            return 1
        elif a== 0 and b==1:
            return 1
        else:
            return 0
        
class NxorGate(BinaryGate):

    def __init__(self,n):
        super(NxorGate,self).__init__(n)
    
    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 1
        elif a== 0 and b==0:
            return 1
        else:
            return 0

class JKFlipFlop(BinaryGate):
    def __init__(self,n):
        super(JKFlipFlop, self).__init__(n)
        self.q = 0 #Current state of flip flop
        self.qn = 0 #Next state on a new clock tick
        self.visited = False #If the flip flop has already been visited
    
    def performGateLogic(self):
        if self.visited: 
            return self.q
        #If the flip flop has already been visited, then it will just return its current state
        self.visited = True

        j = self.getPinA()
        #Main problem here has been solved
        #The function will dig deep to get j's value
        #At some point it asks for its own output, but visited now = True
        #So the code will return its current state
        #Then the code will eventually return back here and continue to evalutate the value of qn
        k = self.getPinB()
        
        if self.q == 0:
            if j == 1:
                self.qn = 1
        else:
            if k == 1:
                self.qn = 0
        #The logic of the gate to evaluate
        return self.q
        #Returns the current state

def main():           
    while True:
        button_press = int(input("Button Pressed? "))
        #Each loop imitates a clock tick
        s1.pin = None
        #Resets the button input
        if button_press == 1:
            b_pressed = Connector(bpY,s1)
            #Connects switch to power
        else:
            b_not_pressed = Connector(bpN, s1)
            #Connets switch to ground
        jk1.q = jk1.qn
        jk2.q = jk2.qn
        #Updates both the flip flop before the circuit is ran for this clock tick
        jk1.visited = False
        jk2.visited = False
        #Resets the visited value for both flip flops
        print(final.getOutput())
        #Runs the circuit for this tick

bpY = Power("Button Press")
bpN = Ground("No button Press")
s1 = Switch("sw1")
p1 = Power("po1")
g1 = AndGate("and1")
g2 = NotGate("not2")
g3 = AndGate("and3")
g4 = NotGate("jk output")
final = AndGate("final")
jk1 = JKFlipFlop("jk1")
jk2 = JKFlipFlop("jk2")

c1 = Connector(s1,g1)
c2 = Connector(s1,g2)
c3 = Connector(s1,g3)
c4 = Connector(g1,jk1)
c5 = Connector(g2, jk1)
c6 = Connector (g3, jk2)
c7 = Connector(p1, jk2)
c8 = Connector(jk1, g4)
c9 = Connector(g4, g3)    
c10 = Connector(jk2, g1)
c11 = Connector(g4, final)
c12 = Connector(jk2, final)
main()
