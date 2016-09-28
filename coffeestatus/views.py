from django.conf import settings
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from webcam.models import Picture
from coffeestatus.serializers import CommandSerializer
from collections import OrderedDict
import random


class CoffeeStatusView(views.APIView):

    serializer_class = CommandSerializer

    def post(self, request):
        return self.run_command(request.data)

    def get(self, request):
        return self.run_command(request.query_params)

    def run_command(self, request_data):
        required_token = settings.SLACK_COMMAND_TOKEN
        if required_token not in (request_data.get('token'), None):
            raise ValidationError({"token": "Invalid token"})
        request = self.request
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        response_data = OrderedDict()
        response_data["response_type"] = "in_channel"
        response_data["text"] = random.choice(STATUS_TEXTS)
        response_data["attachments"] = [
            {
                "fallback": "Web camera snapshot",
                "image_url": request.build_absolute_uri(pic.image.url),
                "text": random.choice(COFFEE_FACTS),
            }
            for pic in Picture.objects.order_by('-created_at')[0:1]
        ]
        return Response(response_data, status=200)


STATUS_TEXTS = [
    "Here's what it looks like in the kitchen.",
    "Let's take a look at the kitchen, shall we?",
    "Let's see if there is any coffee!",
    "Oh, you want some coffee?",
    "Did someone say \"coffee\"?",
]

COFFEE_FACTS = [
    "Random coffee fact #1: Energy drinks still don't have as much caffeine as a Starbucks coffee.",
    "Random coffee fact #2: Coffee is the world's second most valuable traded commodity, only behind petroleum.",
    "Random coffee fact #3: Coffee is most effective if consumed between 9:30 am and 11:30 am.",
    "Random coffee fact #4: The world consumes close to 2.25 billion cups of coffee every day.",
    "Random coffee fact #5: There is a Cat Cafe where you can go to drink coffee and hang out with cats for hours.",
    "Random coffee fact #6: The first webcam was created in Cambridge to check the status of a coffee pot.",
    "Random coffee fact #7: Coffee beans aren't beans. They are fruit pits.",
    "Random coffee fact #8: In the beginning, Starbucks spends more money on health insurance for its employees than on coffee beans.",
    "Random coffee fact #9: Instant Coffee was invented by a man called George Washington around 1910.",
    "Random coffee fact #10: Coffee doesn't taste like it smells because saliva wipes out half of the flavor.",
    "Random coffee fact #11: Drinking a cup of caffeinated coffee significantly improves blood flow.",
    "Random coffee fact #12: There's a Coffee Shop in France where not saying \"hello\" and \"please\" makes your coffee more expensive.",
    "Random coffee fact #13: New Yorkers drink almost 7 times more coffee than other cities in the US.",
    "Random coffee fact #14: One of the world's most expensive coffee brands is made from the dung of Thai elephants.",
    "Random coffee fact #15: 54% of the Americans drink coffee every day.",
    "Random coffee fact #16: If you yelled for 8 years, 7 months and 6 days, you would have produced enough energy to heat one cup of coffee.",
    "Random coffee fact #17: In the beginning, Starbucks only sold roasted whole coffee beans.",
    "Random coffee fact #18: The word \"coffee\" comes from the Arabic for \"wine of the bean\".",
    "Random coffee fact #19: The Netherlands is the world's largest per capita consumer of coffee, averaging 2.4 cups of coffee per person per day.",
    "Random coffee fact #20: Without its smell, coffee would have only a sour or bitter taste due to the organic acids. Try it: hold your nose as you take a sip.",
    "Random coffee fact #21: To study the health effects of coffee, King Gustav III of Sweden commuted the death sentences of a pair of twins on the condition that one drank 3 pots of coffee and the other tea for the rest of their lives.",
    "Random coffee fact #22: The name \"Cappuccino\" comes from the resemblance of the drink to the clothing of the Capuchin monks.",
    "Random coffee fact #23: Americans spend an average of US$1,092 on coffee each year.",
    "Random coffee fact #24: Drinking caffeine in the evening delays our brain's release of melatonin and interrupts our circadian rhythm by as much as 40 minutes.",
    "Random coffee fact #25: If you take caffeine and mix it with sperm in a test tube, it makes the sperm swim better.",
    "Random coffee fact #26: When men drink coffee, Caffeine goes to the semen just like it goes to the blood.",
    "Random coffee fact #27: It has been estimated it would take 70 cups of coffee to kill a 154-pound (70 kg) person.",
    "Random coffee fact #28: Contrary to popular belief, Coffee does not dehydrate you, studies have found.",
    "Random coffee fact #29: Brazil has been the largest producer of coffee for the last 150 years.",
    "Random coffee fact #30: 50% of the caffeine you've consumed may be cleared from your body within 5 hours, but it will take over a day to fully eliminate it from your system.",
    "Random coffee fact #31: Hamburg, Germany, has banned coffee pods from government-run buildings in 2016 because they create unnecessary waste and contain aluminum.",
    "Random coffee fact #32: Two cups of coffee a day were found to reduce the risk of alcohol-related cirrhosis by 43%.",
    "Random coffee fact #33: 20% of office coffee mugs contain fecal bacteria.",
    "Random coffee fact #34: It takes about 37 gallons (140 liters) of water to grow the coffee beans and process them to make one cup of coffee.",
    "Random coffee fact #35: Coffee has been found to reverse liver damage caused by alcohol.",
    "Random coffee fact #36: Drinking 2 to 4 cups of coffee daily has been found to drop the risk of suicide by 50% compared to non-coffee drinkers.",
]
