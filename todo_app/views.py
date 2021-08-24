from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status

from todo_app.serializers import TodoSerializer


class TodoAPIView(APIView):
    #ilk olarak oluşturdugumuz serializeri çağırılcak
    serializer_class = TodoSerializer
    #frontenden gelen bilgileri almak için get methodu oluşturulcak
    def get(self, request, pk=None, format=None):
        """Fetch all records of Todo Resource"""
        with open('db.json') as json_file:
            data = json.load(json_file)
        #eğer sadece isteninlen bilgilere ulaşılmak istencek ise
        if pk:
            print('There is pkkkkkkkkkkkkkk')
            #burda ise sadece bir tane todoya ulaşmak için yazdığımız fonksiyon buluncak
            todo = [item for item in data["items"] if item['id'] == pk]
            return Response({'data': todo})
        

        return Response({'data': data})
    #ikinci olarak yapcağımız post oluşturulcak 
    def post(self, request):
        """Create new Todo Resource"""
        #serializerı oluşturmamızın sebebi bütün dataları çağırcak
        serializer = self.serializer_class(data=request.data)
        #bu kısımda dataları kontrol ediyoruz
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            text = serializer.validated_data.get('text')
            created_at = serializer.validated_data.get('created_at')
            is_complete = serializer.validated_data.get('is_complete')
            #eğer datalar validse yeni todoyu oluşturulcak
            new_todo = {"id": id, "text": text,
                        "created_at": created_at, "is_complete": is_complete}
            #oluşturulan todo todolalrın olduğu klasöre eklencek    
            with open('db.json', 'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data["items"].append(new_todo)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent=4)

            return Response(new_todo, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        # ilk önce pk nin değeri kullanarak jsonının ilgili itemi buluncak
        # frontendden gelen request içinden gelen data serializera gönderilerek validated edilcek.
        # validse item değiştirelecek değilse error dönecek http_404_not_found
        with open('db.json', "r+") as json_file:
            data = json.load(json_file)

        if pk:
            #serializerı oluşturmamızın sebebi bütün dataları çağırcak

            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                #tekrardan istedğiğmiz bilgiyi bulmak için kod yazılcak
                todo = [item for item in data["items"] if item['id'] == pk]
                #update yapacağımız yeni bilgiler girilcek
                id = serializer.validated_data.get('id')
                text = serializer.validated_data.get('text')
                created_at = serializer.validated_data.get('created_at')
                is_complete = serializer.validated_data.get('is_complete')
                #yeni todo oluşturulcak
                new_todo = {"id": id, "text": text,
                            "created_at": created_at, "is_complete": is_complete}
                if todo[0]:
                    #yeni oluşan bilginin id si ile önceki bilginin idsi karşılaştırılcak
                    new_todos = [new_todo if item['id'] ==
                                 new_todo['id'] else item for item in data["items"]]
                    # convert back to json.
                    with open('db.json', 'w') as f:
                        json.dump({"items": new_todos}, f)

                    return Response({"message": "Todo updated"})
                #sistem o idyi bulamazsa not found dönecek
                else:
                    return Response({"message": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):

        with open('db.json', "r+") as json_file:
            data = json.load(json_file)
        #silmek istediğimiz todoya ulaşmak için:
        todo = [item for item in data["items"] if item['id'] == pk]
        #eğer todo id yoksa bad request döncek
        if not todo[0]:
            
            #bura not found olmayacak mi bad request yerine
            return Response({"message": "Bad request"}, status=status.HTTP_404_NOT_FOUND)
        #eğer varsa 
        else:
            
            #burda ise pop methodu ile istenilen idili todoyu silincek
            new_todos = [data['items'].pop() if item['id'] ==
                         pk else item for item in data["items"]]
            # convert back to json.
            with open('db.json', 'w') as f:
                json.dump({"items": new_todos}, f)
            #ve todo deleted döndürülcek
            return Response({"message": "Todo deleted"})
