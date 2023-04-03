import pandas as pd
from elasticsearch import AsyncElasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
name = os.getenv("NAME")
es = AsyncElasticsearch(hosts=f"http://{name}:9200")
mapping = {"properties": {"id": {"type": "integer"}, "text": {"type": "text"}}}



class Elastic:
    async def search(query):
        resp = await es.search(
            index="documents",
            body={"query": {"match": {"text": query}}},
            size=20,
        )
        arr = [i["_source"]["id"] for i in resp["hits"]["hits"]]
        return arr

    async def delete(id):
        try:
            await es.delete_by_query(
                index="documents", body={"query": {"match": {"id": id}}}
            )
            return
        except:
            return

    async def fill():
        if not await es.indices.exists(index="documents"):
            await es.indices.create(
                index="documents", body={"mappings": mapping}
            )
            df = pd.read_csv("posts.csv")
            df = df.reset_index()
            df = df.rename(columns={"index": "id"})
            documents = df.to_dict(orient="records")
            for document in documents:
                await es.index(
                    index="documents",
                    body={"id": document["id"] + 1, "text": document["text"]},
                )
