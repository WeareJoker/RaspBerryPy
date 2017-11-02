# RaspBerryPy
라즈베리파이에서 패킷 스니핑과 동시에, 플러그인을 이용하여 정보를 DB에 저장하는 코드입니다.

## Usage  
## 1. Add plugin  
플러그인을 추가하는 방법은 약간의 규칙을 지켜준다면, 아주 간단합니다!  
1. 기존에 있는 다른 플러그인 폴더를 복사해주세요. _new plugin_ 이름 대신 넣고 싶은 이름을 넣으시면 됩니다.  
![1.png](https://raw.githubusercontent.com/WeareJoker/RaspBerryPy/master/images/1.png)  

2. new plugin 폴더에서, 개발할 때 **_수정할 수_** 있는 파일은 다음과 같습니다.  
	- `handler.py`  
	- `model.py`  
	이 외의 파일을 건드리시면, `pull request` 가 허용되지 않으니, 꼭 기억해주시기 바랍니다.  

	`handler.py` 에서는 패킷에 대한 처리를 담당합니다.  
    `model.py` 에서는 패킷에서 정보를 추출한 후, 저장될 디비 테이블을 담당합니다.  
3. 끝났습니다. 이제 플러그인을 개발해 봅시다.  


`handler.py` 에는 패킷 객체가 옵니다. 안에 내용을 보면  

![2.png](https://raw.githubusercontent.com/WeareJoker/RaspBerryPy/master/images/2.png)  

세션 사용과 packet 변수 처리는 위 이미지 처럼 하면 됩니다.   
다만 반드시 지켜주어야 할 것이 있습니다.  
>**패킷을 처리하는 함수의 경우, 함수 이름을 바탕으로 `CallBack` 루틴에 등록되어 작동합니다.  
따라서 `handler` 라는 함수명과, 파라미터 갯수를 꼭 지켜주어야 합니다.  
다른 함수를 작성하거나, 작성한 함수의 파라미터 조작은 자유롭게 하시면 됩니다.**  


`model.py` 에는 테이블 정의가 이루어집니다. 안에 내용을 보면  

![3.png](https://raw.githubusercontent.com/WeareJoker/RaspBerryPy/master/images/3.png)  

`DNS`는 테이블 정의 클래스입니다. 모든 테이블 정의 클래스는 `Base`를 상속받아 작성해야합니다.  
기존의 클래스 소스를 복붙하여 수정하여도 상관없으니, 크게 신경쓰지 않아도 되는 부분입니다.  

`__tablename__`은 생성될 테이블의 이름을 정의합니다. 위에서는 _dns_ 로 정의 되었습니다.  
> 생성한 테이블에 대해 쿼리를 날릴 때, `select * from dns;` 처럼 날리겠죠?  

`id`, `host` 는 `DNS` 테이블의 멤버 변수로, 각각 컬럼 _(테이블 속성)_ 을 나타냅니다.  
```python
Column(Integer, primary_key=True)
```
에서 `Integer` 는 이 컬럼이 정수임을 알려주고, primary_key 는 `기본 키` 속성으로 테이블 마다 반드시 하나만 존재해야 하는 속성입니다.   
> 테이블에 `primary_key`가 없으면 오류납니다. **_반드시 있어야 하며, 그 갯수는 하나여야만 합니다._**

```python
Column(String(30), nullable=False)
```

`String` 은 이 컬럼이 문자열 컬럼임을, 뒤에 `30`은 길이를 나타냅니다. 문자열 컬럼의 경우 문자열의 크기를 잡아주어야 하는데요, 어떤 데이터가 올 것인지 생각하고 데이터의 길이를 예상하여 적어주어야 합니다.  
`nullable` 은 이 데이터가 `NULL`이면 안된다는 것을 뜻합니다.  

예를 들어   
```python
birth = Column(Date)
```
의 경우 `Date`라는 속성만 있을 뿐, `nullable=False` 속성이 없어 별도의 값이 들어가지 않아도 됩니다.  

여기서 다룬 `primary_key`, `nullable` 외에도 `default`, `unique` 와 같이 다양한 옵션이 존재합니다. 구글링해서 **최대한 자신이 생각한 모델에 가깝게 명시해주는 것이 중요합니다.**


패킷을 분석하고 저장할 `handler`도, 데이터가 저장될 `model`도 다 만들었다면 이제 테스트를 해볼 차례입니다.  

## Database Migrate
`model` 에서 정의된 테이블을 result.db 에 생성해야 합니다. 우리는 이 과정을 `DB Migrate` 라고 부릅니다.  
`Migrate`를 하게되면 우리가 `model`에서 작성된 파이썬 클래스가 디비 쿼리로 변환되어 테이블이 생성되는 과정을 거치게 됩니다.  

방법은 간단합니다.  
`database.py` 파일을 **직접** 실행해주면 됩니다.  

![4.png](https://raw.githubusercontent.com/WeareJoker/RaspBerryPy/master/images/4.png)

없던 result.db 가 생겼습니다!  

## Execute
![5.png](https://raw.githubusercontent.com/WeareJoker/RaspBerryPy/master/images/5.png)


# Thank You :)
