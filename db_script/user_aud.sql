
/*
 select * from  public.user_aud(
null:: integer,
'a':: CHARACTER varying,
'a@gmail.com':: CHARACTER varying,
'123':: CHARACTER varying,
1:: smallint,
'add':: CHARACTER varying
)
*/

create or replace function public.user_aud(
_user_id integer,
_name CHARACTER varying,
_email CHARACTER varying,
_password CHARACTER varying,
_status smallint,
_action CHARACTER varying
)
returns json
LANGUAGE 'plpgsql'  
AS $BODY$

DECLARE 

BEGIN
     
	 if _action = 'add' then 
	 if (select count(1) from public.users where lower(email) = lower(_email)) > 0 then 
	 RAISE EXCEPTION 'User already exists, please login with your existing credentials';
	 end if;
   
	
    INSERT INTO public.users(name,email, password, status,added_date)
    VALUES (_name, lower(_email), _password, 1,now()
    ) returning id into _user_id;
                      
 	RETURN  json_build_object('user_id',_user_id,'message','User registered successfully!','status',1);
	 elseif _action = 'update' then 
	 if _user_id is null then 
	 RETURN  json_build_object('user_id',_user_id,'message','User id is required','status',0);
	 end if;
	 update public.users set 
	password = CASE when _password is null or _password = '' then password else _password end, 
	name = case when _name is null then name else _name end, 
	status = case when _status is null then status else _status end 
	where id = _user_id;
	RETURN  json_build_object('user_id',_user_id,'message','User details updated successfully!','status',1);
	 end if;
    
END;

$BODY$;