#단위테스트
#테스트케이스가 제대로 동작하는지 확인
#기능의 수보다 테스트 케이스 수가 많아야 효과적이다.
#[테스트 결과]
#-> 어떤 부분에 결과와 기대 결과가 다르다.
import unittest
import json
import rest1

class FlaskTest(unittest.TestCase):
    def setUp(self):
        rest1.app.testing = True
        self.client = rest1.app.test_client()
        
    #페이지 동작 테스트
    def test_index(self):
        response = self.client.get('/')
        #self.assertEqual(call, 12) #반환 값 equal? 기대값
        self.assertEqual(response.status_code, 200) #200: Connection Success
        self.assertIn("text/html", response.content_type) 
        self.assertEqual(response.charset, 'utf-8') #Encoding Type

        content = response.data
        self.assertEqual(content.decode('utf-8'), 'hello,Flask!') #문자열 비교

    #Muliply 메소드 동작 테스트
    def test_multiply(self):
        response = self.client.post('/api/multiply?param1=3&param2=4')

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.content_type)
        #json 형식 로드
        json_result = json.loads(response.data)
        self.assertEqual(json_result.get('state'), 1)
        self.assertEqual(json_result.get('response'), 12)

if __name__ == "__main__":
    unittest.main()