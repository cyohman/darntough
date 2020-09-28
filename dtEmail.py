import time
import asyncio
import aiohttp
import os
import filetype
from werkzeug.datastructures import FileStorage
from aiohttp import FormData

EMAIL_URL="http://localhost:5000/email"

queue = []

def createQueue():

    queueFile  = open('queue', 'r')
    
    while True:
       queueEntry = queueFile.readline()

       if not queueEntry:
          break
              
       values = queueEntry.split(',')

       if(len(values)==1):
          queue.append({'email': values[0].strip()})
       else:
          queue.append({'email': values[0].strip(), 'file': values[1].strip()})
         

async def aiohttp_post(queueEntry):


    data=FormData()

    if 'file' in queueEntry:
       filename = queueEntry.get('file')
       my_document  = os.path.join('tests/data/', filename)

       #Not 100% foolproof, but it will do for now
       kind = filetype.guess(my_document)

       data.add_field('file', open(my_document, "rb"), filename=filename, content_type=kind.mime)
       

    data.add_field('recipient', queueEntry.get('email'))

    print("Sending email.")
    async with aiohttp.ClientSession() as session:
        async with session.post(EMAIL_URL, data=data) as response:
            return response

async def post_async(queueEntry):

    response = await aiohttp_post(queueEntry)

    response.close()

async def asynchronous():
    createQueue()    
    tasks = [asyncio.create_task(
        post_async(queue[i])) for i in range(0, len(queue))]
    await asyncio.wait(tasks)

asyncio.run(asynchronous())

