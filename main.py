from typing import Optional

import uvicorn
from fastapi import FastAPI

import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

app = FastAPI()

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    cat = graphene.List(graphene.String) 

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

app.mount("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation), on_get=make_graphiql_handler()))

if __name__ == "__main__":
    print("http://127.0.0.1:1111")
    uvicorn.run(app, host="0.0.0.0", port=1111)