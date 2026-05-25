content = """
I am Yashvardhan Gupta, a passionate software developer with a keen interest in AI and machine learning. 
I have experience working with various programming languages and frameworks, 
and I enjoy building innovative applications that leverage the power of AI to solve real-world problems. 
In my free time, I like to explore new technologies, contribute to open-source projects, and stay updated with the latest trends in the tech industry.   
"""
# A sampletest before going towrds the main code
import time


for l in content:
    print(l, end="",flush=True)
    time.sleep(0.01) # As the content is very less therefore it would print almost instantly so added sleep to make it look like it's being typed out
