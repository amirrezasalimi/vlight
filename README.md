# vlight


simple package for validation data

## Getting Started


### Installing

if you have old version do this:

`pip uninstall vlight`

and to install latest version :
`pip install vlight`


#### use vlight


```python
from vlight import v
```


### examples

validate a simple login form with email :

```python
from vlight import valid # also you can use "v" helper method
```


#### vlight in django

`create validation rules and set data`
```python
from vlight import v
valid = v({
    "email": "req|email",
    "password": "req|min:8|max:255"
}, data={
    "email":"test@gmail.com",
    "password": "123" # this field have minimum character error
})
#check data is valid

if valid.isOk():
    # submit your form
    pass

error=valid.errors()
#check have error
if valid.fails():
    msgs=error.all()

#check a field have error

if error.has("email"):
    #this block run when your email field have error
    pass

#get field errors messages
print(error.get("email"))
# you can set returned error length
print(error.get("email",2)) 


#customize error messages

#to customize all fields default messages:
valid = v({
    "email": "required|email",
    "password": "required|min:8|max:255"
}, data={
    "email":"test@gmail.com",
    "password": "123"
},messages={
    "required":"{field} required ",
    "email": "email field with value [{value}] not valid",
 }
)

#or you can customize only a field messages
valid = v({
    "email": "required|email"
    "|required.msg:enter your email"
    "|email.msg:email is not valid",
    
    "password": "required|min:8|max:255"
    "|str.min:your password is easy"
    "|str.max:your selected password so hard"
}, data={
    "email":"test@gmail.com",
    "password": "123"
})
```



 
##### an example in django

`views.py`
```
from django.shortcuts import render
from vlight import v

def index(request, **kwargs):
    msgs = []
    if request.method == "POST":
    
        valid = v({
            "email": "required|email",
            "password": "required|min:8|max:255"
        }, data=request.POST)
        
        if valid.fails():
            msgs = valid.errors().all()
        else:
            msgs.append("your form submitted!")
            
    return render(request, "index.html", {"login_errors": msgs}) 
```
`index.html`  jinja2
```
<form action="/" method="post">
    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
    <label for="email">email:</label>
    <input id="email" type="text" name="email">
    <br>
    <label for="password">password:</label>
    <input id="password" type="password" name="password">
    <input type="submit" value="login">
    {% for error in login_errors %}
        <li><a href="#">{{ error }}</a></li>
    {% endfor %}
</form>
```

#### supported rules

`required` check data has field and data is not empty
```
"required"
```
`email`  pattern : `^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`
```
"email"
```

`ip`  pattern : `^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$`
```
"ip"
```

`url` pattern : `^http(s?):\/\/(www\.)?(((\w+(([\.\-]{1}([a-z]{2,})+)+)(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)|(\w+((\.([a-z]{2,})+)+)(\:[0-9]{1,5}(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)))|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(([0-9]|([1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]+)+)(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*)((\:[0-9]{1,5}(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)*))$`
```
"url"
```

`not_in` `in` check value in items
```
"in:small,larg"
```



`regex`
`not_regex` coming soon


`ext` check path extension 
```
"ext:jpg,png,jpeg"
```

`int` integer validation
```
"int"
```
`max` set maximum character of string
```
"max:255"
```
and you can change the rule for int value to check max integer value
```
"int|max:255"
```





##### [ more validation rules will added coming soon ]




#### develop your rule

`docs coming soon`

#### latest version changes

`0.1`
- fix bugs

# contact  

- telegram: https://t.me/Amir_s365
- gmail: amirrezasalimi0@gmail.com


# License


This project is licensed under the MIT License
