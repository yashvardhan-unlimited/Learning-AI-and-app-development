# Asycnio/Aiohttp
I learned Use of Async and Await pretty much also used Aiohttp module instead of regular requests modulte for accessing the web.

I made a downloader program, you just need to put links in the urls list and filename in filename list, and the files will get downloaded.
for this we tried three things
First (sync_app.py) - Normal Syncrounus approach with request module
Second (async_app.py) - We used the aiohttps module but still the the program was syncrounus 
third (async_app2.py) - We used the asyncrounus approach and downloaded the files faster. 

The experiment went sucessfull

NOTE: make sure you dont put a lot of links of same website in async_app2.py the third approach as all the requests go to the web at one the web may return rate limit and slowdown your process.

Please do suggest any different approach you have to get better results, please confirm if my NOTE is correct or something else I am mssing.