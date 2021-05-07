from typing import Optional

from fastapi import FastAPI

import graphene
from starlette.graphql import GraphQLApp

app = FastAPI()

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    cat = graphene.List(graphene.String, type_=graphene.String()) 

    def resolve_cat(self, info, **input):
        if input["type_"] == "white":
            return ["white cat"]
        else:
            return ["black cat"]

    def resolve_hello(self, info, name):
        return "Hello " + name

class Person(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    real_name = graphene.String()
    fake_name = graphene.String()

    def mutate(root, info, **input):
        the_name = input["name"]
        return {"real_name":f"MR. {the_name}", "fake_name":f"fake. {the_name}"}


class Mutation(graphene.ObjectType):
  create_person = Person.Field()


@app.get("/")
def read_root():
    return {"Hello": "World", "name": "yingshaoxo"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))
