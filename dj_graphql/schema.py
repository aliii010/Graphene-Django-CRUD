import graphene
import graphql_crud.schema

class Query(graphql_crud.schema.Query):
  pass

class Mutation(graphql_crud.schema.Mutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)