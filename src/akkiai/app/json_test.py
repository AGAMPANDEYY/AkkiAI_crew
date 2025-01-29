import json 

#json_string="{\n  \"buyer_persona\": {\n    \"name\": \"Sarah, the Busy Mid-Career Professional\",\n    \"narrative\": \"Sarah is a 32-year-old marketing manager at a growing SaaS company. She has a bachelor's degree and 7 years of experience in her field. Sarah lives in a suburban area with her husband and young child. She feels overwhelmed by the demands of her job, household responsibilities, and maintaining a healthy lifestyle. Sarah is highly motivated to find solutions that will help her achieve better work-life balance and improve her overall quality of life.\",\n    \"demographic_information\": \"Age: 28-35 years old, Gender: Female, Income Range: $50,000 - $80,000 per year, Location: Urban and suburban areas, Education Level: Bachelor's degree, Occupation: Mid-level professionals, such as marketing managers, HR specialists, and small business owners.\",\n    \"psychographic_information\": \"Interests & Hobbies: Fitness, wellness, personal development, home decor, cooking, and spending time with friends and family. Motivations: Achieving a healthy work-life balance, professional advancement, and improving their overall quality of life. Aspirations: To feel confident, productive, and in control of their personal and professional lives. Fears & Challenges: Feeling overwhelmed by the demands of work, home, and social commitments; struggling to maintain a healthy lifestyle; and uncertainty about the future.\",\n    \"behavioral_information\": \"Free Time Activities: Exercising (e.g., yoga, cycling, running), reading self-help books, browsing home decor websites, and socializing with friends. Social Media Usage: Active on Instagram, Facebook, and LinkedIn to stay connected with friends, follow influencers, and engage with brands. Purchasing Habits: Tend to be planned and research-driven, but will also make impulsive purchases for self-care or treating themselves. Brand Engagement: Enjoy personalized email communications, interactive social media content, and in-person events or workshops.\",\n    \"buying_process\": \"Sarah's buying decision process is thorough and research-driven. She will extensively research online (reviews, comparison sites, brand websites), seek recommendations from friends and family, and be willing to pay a premium for quality products or services that align with her personal values and lifestyle. The buying decision may involve multiple stakeholders, including her manager, HR team, and potentially IT or finance departments.\",\n    \"consumption_patterns\": \"Sarah consumes similar products and services, such as fitness apps, meal delivery services, productivity tools, and home organization products. She values convenience, efficiency, aesthetics, and alignment with her personal values and lifestyle when making purchasing decisions.\",\n    \"aspirations\": \"Sarah's primary aspirations are to achieve a healthy work-life balance, advance her career, and improve her overall quality of life. Solving her challenges around feeling overwhelmed and maintaining a healthy lifestyle would help her feel more confident, productive, and in control of her personal and professional life.\"\n  }\n}"
json_string= "{\n  \"jtbd_analysis\": \"a. The main 'job' the customer (Sarah) is trying to accomplish by using this product/service is to achieve better work-life balance and improve her overall quality of life. She feels overwhelmed by the demands of her job, household responsibilities, and maintaining a healthy lifestyle.b. The problem or pain point Sarah is trying to solve with this product/service is feeling a lack of control and struggling to maintain a healthy lifestyle amidst her busy schedule.c. The outcome Sarah hopes to achieve after using this product/service is to feel more confident, productive, and in control of her personal and professional life.d. The obstacles or frustrations Sarah experiences while trying to get this job done include feeling overwhelmed by the demands of work, home, and social commitments, as well as uncertainty about the future.e. Sarah would choose this product/service over alternatives because it aligns with her personal values and lifestyle, providing convenience, efficiency, and aesthetics to help her achieve her goal of better work-life balance.\",\n  \"jtbd_statement\": \"This product/service helps busy mid-career professionals like Sarah accomplish the 'job' of achieving better work-life balance and improving their overall quality of life. By addressing their pain points around feeling overwhelmed and struggling to maintain a healthy lifestyle, it enables customers to feel more confident, productive, and in control of their personal and professional lives.\"\n}"
json_string="{\n  \"stages_of_awareness_analysis\": {\n    \"unaware\": \"Based on the information provided, it is estimated that approximately 30% of the target audience may be in the Unaware stage. This segment of the audience does not yet recognize that they have a problem around work-life balance and maintaining a healthy lifestyle. They may be content with their current situation or simply not aware of the challenges they face. To reach this audience, the marketing strategy should focus on raising awareness about the common issues mid-career professionals like Sarah experience, such as feeling overwhelmed by the demands of work, home, and personal responsibilities. Messaging should educate this audience on the importance of achieving better work-life balance and highlight the negative impacts of not addressing these problems.\",\n    \"problem_aware\": \"Around 40% of the target audience may be in the Problem Aware stage. This segment recognizes that they are struggling to maintain a healthy work-life balance and lifestyle, but they may not yet be aware of the specific solutions available to them. The key messages for this stage should focus on validating the audience's pain points and challenges, while also introducing the concept that there are products and services that can help address these problems. Effective marketing channels for this stage may include industry publications, social media forums, and targeted email campaigns that provide valuable content and resources related to work-life balance and personal wellness.\",\n    \"solution_aware\": \"Approximately 20% of the target audience may be in the Solution Aware stage. These individuals understand that there are products and services available to help them achieve better work-life balance, but they may not yet be familiar with the specific offering. Marketing efforts for this stage should highlight the features and benefits of the product/service, showcase how it can address the audience's pain points, and provide social proof through customer testimonials or case studies. Channels like the company's website, content marketing, and targeted social media advertising may be particularly effective in reaching this audience.\",\n    \"product_aware\": \"Around 8% of the target audience may be in the Product Aware stage. These individuals are familiar with the product/service and understand how it can help them, but they may still have some reservations or questions about whether it is the right fit for their needs. Marketing strategies for this stage should focus on addressing any remaining concerns or objections, providing detailed product information, and making it easy for the audience to take the next step in the buying process. This may include offering free trials, consultations, or personalized recommendations.\",\n    \"most_aware\": \"Approximately 2% of the target audience may be in the Most Aware stage. These individuals are well-informed about the product/service, its features, and how it can address their specific needs. They are almost ready to make a purchase. Marketing efforts for this stage should aim to convert these leads into customers by emphasizing the unique value proposition, providing a seamless buying experience, and offering any relevant incentives or promotions.\"\n  },\n  \"summary_and_recommendations\": \"Based on the Stages of Awareness analysis, it is clear that the target audience has varying levels of awareness about their problems and the available solutions. To effectively guide them through the purchase journey, a multi-faceted marketing strategy is recommended:1. For the Unaware and Problem Aware segments, focus on raising awareness and educating the audience about the importance of achieving better work-life balance and maintaining a healthy lifestyle. Utilize content marketing, social media, and industry publications to reach this audience.2. For the Solution Aware and Product Aware segments, emphasize the features, benefits, and unique value proposition of the product/service. Showcase customer success stories, provide detailed product information, and address any remaining concerns or objections.3. Optimize the buying experience for the Most Aware segment, ensuring a seamless and personalized customer journey that encourages them to take the final step and make a purchase. Consider offering incentives, promotions, or personalized recommendations to convert these leads.4. Continuously monitor and analyze customer behavior and feedback to refine the marketing strategies and messaging across the different stages of awareness. Adapt and optimize the approach as needed to effectively guide the target audience through the purchase funnel.By implementing a tailored marketing strategy based on this Stages of Awareness analysis, the business can effectively reach and engage customers at various levels of awareness, ultimately driving more conversions and building a loyal customer base.\"\n}"
parsed_json=json.loads(json_string)

print(parsed_json)