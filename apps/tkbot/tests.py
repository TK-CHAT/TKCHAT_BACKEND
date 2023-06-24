from django.test import TestCase

# Create your tests here.
# from rest_framework.test import APITestCase
# from rest_framework.reverse import reverse
# from apps.tkbot.models import BotPrompts

# class BotPromptsCRUDTests(APITestCase):
#     def test_create_botprompt(self):
#         url = reverse('create_prompt')
#         data = {'bot': 1, 'prompt': 'Test prompt', 'role': 'ASSISTANT'}
#         response = self.client.post(url, data)
#         print(dir(response))
#         print(response.content)
#         print(response.data)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(BotPrompts.objects.count(), 1)
#         self.assertEqual(BotPrompts.objects.get().prompt, 'Test prompt')