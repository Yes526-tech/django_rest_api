import json  
data = [{
    "id": 1,
    "text": "Learn about Polymer",
    "created_at": "Mon Apr 26 06:01:55 +0000 2015",
    "Tags": [
        "Web Development",
        "Web Components"
    ],
    "is_complete": True
},
{
    "id": 2,
    "text": "Learn about Python",
    "created_at": "Tue Apr 26 06:01:55 +0000 2015",
    "Tags": [
        "Web Development",
        "Web Components",
        "Django"
    ],
    "is_complete": False
}]

with open('db.json', 'w') as file:
    json.dump(data, file) 