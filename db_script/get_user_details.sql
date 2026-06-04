
/*
select * from  public.get_user_details(
    9::integer)
	
*/
CREATE OR REPLACE FUNCTION public.get_user_details(
    _user_id integer)
    returns table(name character varying,email character varying,id integer,status smallint,added_date date)
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    BEGIN
	return query
	select u.name,u.email,u.id,u.status ,u.added_date::date from public.users u where u.id= _user_id;
    END;

$BODY$;

