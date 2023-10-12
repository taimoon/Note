from dataclasses import dataclass
@dataclass
class Exp: ...

Val = int|float|bool
Expr = Exp|Val

@dataclass
class BinOp(Exp):
    left:Expr
    right:Expr

@dataclass
class Add(BinOp): ...

@dataclass
class Sub(BinOp): ...

@dataclass
class Mul(BinOp): ...

@dataclass
class Div(BinOp): ...


@dataclass
class Var:
    id:str

@dataclass
class Let:
    var:Var
    val:Exp
    body:Exp

@dataclass
class Proc(Exp):
    param:str
    body:Expr

@dataclass
class App(Exp):
    op:Expr
    arg:Expr
    
@dataclass
class Lt(BinOp): ...
@dataclass
class Gt(BinOp): ...
@dataclass
class Le(BinOp): ...
@dataclass
class Ge(BinOp): ...
@dataclass
class Eq(BinOp): ...

@dataclass
class If(Exp):
    pred:Expr
    conseq:Expr
    alter:Expr

@dataclass
class UnaryOp(Exp):
    e:Expr

@dataclass
class Not(UnaryOp):...
@dataclass
class And(BinOp):...
@dataclass
class Or(BinOp):...

@dataclass
class Cond(Exp):
    clauses:list[list[Expr,Expr]]


from dataclasses import dataclass
@dataclass
class Env:
    env:list[list[str,int|float]]
    def apply(self,var:str):
        match self:
            case Env([]):
                raise NameError()
            case Env([[x,v],*xs]) if x==var:
                return v
            case Env([_,*xs]):
                return Env([*xs]).apply(var)
    
    def extend(self,var:str,val:Val):
        return Env([(var,val),*self.env])

def create_env() -> Env:
    return Env([])

def apply_env(var:str,env:Env) -> Val:
    return env.apply(var)

def extend_env(var:str,v:Val,env:Env) -> Env:
    return env.extend(var,v)

def expand(e):
    match e:
        case int()|float()|bool()|Var():
            return e
        case And(left,right):
            return expand(If(left,right,False))
        case Or(left,right):
            return expand(If(left,True,right))
        case If(Not(pred),conseq,alter):
            return expand(If(pred,alter,conseq))
        case If(True,conseq,_):
            return expand(conseq)
        case If(False,_,alter):
            return expand(alter)
        case If(pred,conseq,alter):
            return If(expand(pred),expand(conseq),expand(alter))
        case Cond([[pred,conseq],alter]):
            return expand(If(pred,conseq,alter))
        case Cond([[pred,conseq]]):
            return expand(If(pred,conseq,False))
        case Cond([[pred,conseq],*clauses]):
            return expand(If(pred,conseq,Cond([*clauses])))
        case Let(str(id),val,body):
            return expand(App(Proc(id,body),val))
        case App(op,arg):
            return App(expand(op),expand(arg))
        case Proc(param,body):
            return Proc(param,expand(body))
        case BinOp(left,right):
            return e.__class__(expand(left),expand(right))
        case _:
            raise NotImplementedError('expander, unexpected ',e)


def interp(e,env):
    match e:
        case int(x)|float(x)|bool(x):
            return x
        case Mul(left,right):
            return interp(left,env) * interp(right,env)
        case Add(left,right):
            return interp(left,env) + interp(right,env)
        case Sub(left,right):
            return interp(left,env) - interp(right,env)
        case Div(left,right):
            return interp(left,env) / interp(right,env)
        case Let(str(id),val,body):
            return interp(body,extend_env(id,interp(val,env),env))
        case Proc(params,body):
            return Proc(params,body)
        case Var(id):
            return apply_env(id,env)
        case App(op,arg):
            match interp(op,env):
                case Proc(param,body):
                    return interp(body,extend_env(param,interp(arg,env),env))
        case Lt(left,right):
            return interp(left,env) < interp(right,env)
        case Gt(left,right):
            return interp(left,env) > interp(right,env)
        case Le(left,right):
            return interp(left,env) <= interp(right,env)
        case Ge(left,right):
            return interp(left,env) >= interp(right,env)
        case Eq(left,right):
            return interp(left,env) == interp(right,env)
        case If(pred,conseq,alter):
            if interp(pred,env) is True:
                return interp(conseq,env)
            else:
                return interp(alter,env)
        case _:
            raise NotImplementedError('interp, unexpected argument', e)