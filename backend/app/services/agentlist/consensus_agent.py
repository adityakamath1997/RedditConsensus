from agents import Agent, Runner, function_tool, TResponseInputItem, ModelSettings
from datetime import datetime
from backend.app.schemas.consensus_agent import ConsensusOutput
import asyncio

class ConsensusAgent:
    def __init__(self, original_query):
        self.agent = Agent(
            name="Consensus Generator",
            instructions=self._get_instructions(),
            model="o4-mini",
            output_type=ConsensusOutput
        )
        self.original_query = original_query
        

    def _get_instructions(self):
        consensus_finder_instructions = """
You are a helpful assistant that will answer a user query from relevant reddit posts. You will be details of several relevant reddit posts.
Each posts details will be preceded by a post number (eg. POST 1) and the details will be structured in the following manner:
1. Post title
2. Post description
3. A list of the top 20 parent comments, sorted in descending order of their number of upvotes.

Your goal is to get a consensus of the comments in the posts provided and try and answer the users original query.

Take into consideration the following factors while arriving at a consensus:
1. How relevant is the post body to the users question
2. The helpful top comments and the number of upvotes they have.
3. Filter out any comments that seem like satire/sarcasm/comedy or are generally unhelpful.

Answer the users original question and make sure to mention that the answer is a consensus of what reddit users think.

You will output your answer, as well some additional information:
1. 2-3 Reasons to justify your answer
2. 0-3 Caveats/Warnings to the user who is looking at this information. Make sure this is only about the source of the information. Examples might be few relevant posts/comments, or if some of the information seems sponsored etc.
"""
        return consensus_finder_instructions
    
    async def get_consensus(self, post_details):
        query = f"Original Query: '{self.original_query}' Posts details: {post_details}"
        response = await Runner.run(self.agent, query)
        return response.final_output
    
if __name__ == "__main__":
    POST_DETAILS = ["POST 1:\nTitle: I need a good budget gaming laptop\nAuthor: Shadow_spire1234\nContent: I want a laptop for college and want to continue website development and want to learn game development. I also plan for some occasional gaming. I also want to try ml and ai on this laptop but don't have the proper funds, I also want a decent battery life 3 to 5 hours for coding that's it. My budget is 80000inr(1000usd) (I just relocated from Chicago to India afew  years ago and  am in desperate need of a laptop) if u guys have any good suggestions pls tell me.\n\nMin Specs:\n\nAmd 5 or 7(7 is ideal)\nRtx 3050 6gb \n16 gb ram\n512 gb ssd \nALL IN ALL GOOD GAMING LAPTOP WITH GOOD BATTERY BACKUP AND UNDER 1000 USD AVAILABLE IN INDA.\n\n\n\nTop Comments:\n1. (1 upvotes) Asus tuf a15 rtx4060 or rtx4070\n2. (1 upvotes) Yeah me too, my brother also has a loq so I'm leaning towards it, also the a15 4050 is out of my  budget\n", "POST 2:\nTitle: What are the best gaming laptops that are affordable.\nAuthor: Ahmed-_-Nasr\nContent: Hey everyone! I’m looking to buy a laptop that I’ll use mainly for programming, university work, and some gaming. So far, I’ve been considering options like the Lenovo LOQ.\n\nFrom what I’ve gathered, I should be aiming for at least *16GB DDR5 RAM*, *SSD storage*, and a *144Hz display*. For the GPU, I’m looking at something like the *RTX 4050 or better*.\n\nI don’t game heavily, and when I do, it’s usually on less demanding titles—but I’d still like the option to play more intensive games like The Witcher or God of War if I ever feel like it.\n\nAre there any important specs I might be overlooking? Any good value recommendations around this performance tier would be appreciated!\n\nTop Comments:\n1. (9 upvotes) Never aim for 4050 in laptops, always go 4060/ti or higher, as a laptop GPU is never 1 to 1 with desktop GPUs. \n\nAlso, 8GB VRAM is not a lot these days, but if you’re gaming on 1080p, then it should be fine. If you want future proofing as well as being able to comfortably play AAA games, aim for 12GB VRAM or above\n\nThe rest is up to your preference. Do lots of research!!! Do not jump straight into 1 laptop. Watch reviews, scroll on these forums too:)\n2. (8 upvotes) Lenovo LOQ ones are pretty good, if you wanna check them out. A lot of them are on sale right now on their website.\n3. (2 upvotes) oh, the Lenovo LOQ is a solid choice for sure! for programming and casual gaming, those specs (16GB DDR5, SSD, 144Hz, RTX 4050+) are pretty much spot on, but definitely also check out the Acer Nitro V or even some of the ASUS TUF models, they often pop up with similar configs at great price points, and sometimes even a slightly better cooling solution, which is always a plus\n4. (2 upvotes) Also a light gamer (only mess with cod and sim games) i love my 4060 loq does exactly what i need it to do keeps good temp and doesn't lag, one great place i check religiously for good pricing is best buy open box ended up getting mine for about 650 before taxes and i didn't even need to order it i just picked it up after work one day\n5. (1 upvotes) i was also considering buying the loq at first but i got a sweet deal of few thousand more and got the omen.  \ntotal beast I am very satisfied with it, but i just want to ask fellow gamers(this is my first gaming laptop) how much is your battery life(both while gaming and usual task) ?\n6. (1 upvotes) I picked up an Asus Zepherus g14 on black Friday for $1200 and I love that computer\n7. (1 upvotes) What’s your budget and what country are you in? Prices vary quite a lot by region.\n", "POST 3:\nTitle: Best budget gaming laptop\nAuthor: Aranel87\nContent: Hello,\nI am looking for a budget laptop with rtx 4070. \nMy main concern is built quality and weight.\nI will be mostly using it for creating visual content with ai better gpu is important.\nI was looking at msi karana 15 or hp victus series. \nLaptops with metal casing are too expensive,\nWhat would you recommend?\n\nThanks in advance.\n\nTop Comments:\n1. (7 upvotes) Ive seen the katana being really bad as people say here.\n\nIm prone to buying sword 17hx myself because i can get it for about 1000usd which is a steal here in europe. But i still cant get over few things\n2. (2 upvotes) If you are looking for other budget brands outside of MSI's offerings,  I would consider Gigabyte and a German manufacturer called Medion (may not be available much in the US).  I would opt for either of those before an MSI Katana, Cyborg or Thin.... given the things I've heard.\n\nGigabyte G5 and G6 series get very good reviews, especially by the standards of budget laptops.  I made an informed decision on mine when my 3070 Ti met an unfortunate end and for 800 bucks I'm now getting about the same performance from a 4060.\n\nI will probably stick with Gigabyte now when I get my next laptop which will be more mid-range.\n\nIf I was buying budget right now, I'd probably go for something like this:\n\n[https://www.currys.co.uk/products/gigabyte-g6-16-gaming-laptop-intel-core-i7-rtx-4060-1-tb-ssd-10261810.html](https://www.currys.co.uk/products/gigabyte-g6-16-gaming-laptop-intel-core-i7-rtx-4060-1-tb-ssd-10261810.html)\n3. (1 upvotes) What's the budget and location?\n4. (1 upvotes) What country are you in and what’s your budget?\n", 'POST 4:\nTitle: Best gaming laptop under 1100$ (Strict Budget)\nAuthor: THE-FATE\nContent: Long story short, I\'m selling my gaming computer to get a gaming laptop for portability.\n\nPC specs:\ni3 - 13100f\nMSI PRO Z690-A WiFi\nADATA 1TB SSD M.2\nLexar 256GB M.2\nXPG Lexar 32GB DDR5 (5200mhz)\nLian Li o11 Dynamic Mini\nThermalright TL-S12 x8 \nDeepcool Ak400 Digital\nMsi Rtx 3070 Gaming Trio \n\nI sold this computer for 1000$ in my country. I\'m buying a laptop from USA (Used or new). \n\nConcerns:\n1) Generally laptops under 1100$ have i9 11th gen or i7s with Rtx 4060/4070. Is it gonna be better then my PC or worse?\n2) What is the best laptop under 1100$ used or new doesn\'t matter?\n\nMy requirements:\n1) There are many good options but they look so bulky and alien devices. I want something slim and elegant like the ROG Zephyrus G14 and Razer Blade 16.\n2) Rtx 4060 or 4070\n3) At least 1TB M.2\n4) New or used in open box or barely used condition.\n\nCurrent Picks: (Used/Ebay)\n1: ASUS - ROG Zephyrus G14 14" OLED 3K 120Hz  - AMD Ryzen 9 8945HS - 16GB RAM - RTX 4060\n2: GIGABYTE G6X 16" 165Hz IPS Intel - i7-13650HX - 32GB RAM - RTX 4060\n\nTop Comments:\n1. (11 upvotes) hp omen transcend/acer predator helios 14/asus tuf a14/zephyrus g14/razer blade 14\n\nhttps://preview.redd.it/2b1oeoqlqa1f1.png?width=1634&format=png&auto=webp&s=d1a8d1a8f75f900fff77600227b1595c38eb3afd\n\nwait for a sale on bestbuy for the 4060, should drop to 1k soon (memorial day sale?)\n2. (6 upvotes) Zephyrus G14 all the way\n3. (1 upvotes) I\'d definitely consider the Zephryus G14.\n\nThat gigabyte has a poor screen and chassis flex issues.\n']
    async def main():
        consensus_agent = ConsensusAgent(original_query="Best budget gaming laptops")
        answer = await consensus_agent.get_consensus(POST_DETAILS)
        print(answer)

    asyncio.run(main())
        
