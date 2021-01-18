import graphene

class Test(graphene.Mutation):
    member = graphene.String()
    generated_password = graphene.String()

    class Arguments:
        token = graphene.String(required=False)
        
    def mutate(self, info, **kwargs):
        return Test(member="member", generated_password="password")
      
class Mutation(graphene.ObjectType):
    test = Test.Field()