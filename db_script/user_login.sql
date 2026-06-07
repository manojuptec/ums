
/*
select * from  public.user_login_logout(
    null::integer,
	'a@gmail.com':: character varying,
	'123':: character varying,
	'asdrt':: character varying,
	null:: text[],
	'login'::character varying)
*/
CREATE OR REPLACE FUNCTION public.user_login_logout(
    _logged_user_id integer,
	_email character varying,
	_login_password character varying,
	_token character varying,
	_sessioninfo text[],
	_action character varying)
    returns json
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_user_id integer;
    _password character varying;
    _status smallint;
    _is_logged_in smallint;
	_roleID integer;
	_is_verified boolean;
	_name character varying;
	_added_date date;
    BEGIN
	if _action ='login' then 
      SELECT id, password, status,name,added_date into _user_id, _password, _status,_name,_added_date
      from public.users 
      where 
      	lower(email) = lower(_email);  
      
      if _user_id is null then
      	RAISE EXCEPTION 'Invalid login-id --> %', _email
					USING HINT = 'User does not exist';
      end if;
      
	 
      if _password <> _login_password then
      	RAISE EXCEPTION 'Invalid password';
      end if;
	 
	 
      -- Insert new entry for current device
	  INSERT INTO user_token (user_id, token) 
	  VALUES (_user_id, _token);
      	RETURN  json_build_object('id',_user_id, 'status',_status,'name',_name,'added_date',_added_date,'email',_email,'message','User logged in successfully!','status',1);  
     elseif _action = 'logout' then 
      if _logged_user_id is null  then 
	 RAISE EXCEPTION 'User id is required';
	 end if;
	 delete from user_token where user_id=_logged_user_id and token = _token;
	 RETURN  json_build_object('user_id',_logged_user_id,'message','User logged out successfully!','status',1);  
    end if;	 
    END;

$BODY$;

