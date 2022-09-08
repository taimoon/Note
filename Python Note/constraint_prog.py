class Connector:
    def __init__(self):
        self.informant = None
        self.val = None
        self.constraints = []

    def has_val(self):
        return self.informant is not None

    def connect(self, new_constraint):
        if new_constraint not in self.constraints:
            self.constraints.append(new_constraint)
        if self.has_val():
            new_constraint.process_new_val()

    def set_val(self, new_val, setter):
        if not self.has_val():
            self.val = new_val
            self.informant = setter
            for inst in self.constraints:
                if inst == setter: continue
                inst.process_new_val()
        elif self.val != new_val:
            raise Exception(f"Contradiction {self.val} {new_val}")
        else:
            return None

    def forget_val(self, retractor):
        if retractor == self.informant:
            self.informant = None
            for inst in self.constraints:
                if inst != retractor:
                    inst.process_forget_val()
        return None

    def __repr__(self):
        return str(self.val)


class Constant:
    def __init__(self, val, conn):
        conn.connect(self)
        conn.set_val(val, self)

class Adder:
    def __init__(self, a1: Connector, a2: Connector, sum: Connector):
        self.a1 = a1
        self.a2 = a2
        self.sum = sum
        self.a1.connect(self)
        self.a2.connect(self)
        self.sum.connect(self)


    def process_new_val(self):
        if self.a1.has_val() and self.a2.has_val():
            self.sum.set_val(self.a1.val+self.a2.val, self)
        elif self.sum.has_val() and self.a1.has_val():
            self.a2.set_val(self.sum.val-self.a1.val, self)
        elif self.sum.has_val() and self.a2.has_val():
            self.a1.set_val(self.sum.val-self.a2.val, self)


    def process_forget_val(self):
        self.a2.forget_val(self)
        self.a2.forget_val(self)
        self.sum.forget_val(self)
        self.process_new_val()


    def __repr__(self):
        return f"Adder(a1={self.a1.val},a2={self.a2.val},sum={self.sum.val})"

class Multiplier:
    def __init__(self, m1: Connector, m2:Connector, prod:Connector):
        self.m1 = m1
        self.m2 = m2
        self.prod = prod
        self.m1.connect(self)
        self.m2.connect(self)
        self.prod.connect(self)

    def process_new_val(self):
        if self.m1.has_val() and self.m1.val == 0:
            self.prod.set_val(0, self)
        elif self.m2.has_val() and self.m2.val == 0:
            self.prod.set_val(0, self)
        elif self.m1.has_val() and self.m2.has_val():
            self.prod.set_val(self.m1.val*self.m2.val, self)
        elif self.prod.has_val() and self.m1.has_val():
            self.m2.set_val(self.prod.val / self.m1.val, self)
        elif self.prod.has_val() and self.m2.has_val():
            self.m1.set_val(self.prod.val / self.m2.val, self)

    def process_forget_val(self):
        self.m1.forget_val(self)
        self.m2.forget_val(self)
        self.prod.forget_val(self)
        self.process_new_val()

    def __repr__(self):
        return f"Multiplier(m1={self.m1.val},m2={self.m2.val},prod={self.prod.val})"
