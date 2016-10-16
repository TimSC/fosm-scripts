;
%gtmaccess	; entry points to access GT.M
	quit
	;
get(var,value,error)
	set value=@var
	quit:$quit 0 quit
	;
init(error)
	set $ztrap="new tmp set error=$ecode set tmp=$piece($ecode,"","",2) quit:$quit $extract(tmp,2,$length(tmp)) quit"
	quit:$quit 0 quit
	;
kill(var,error)
	kill @var
	quit:$quit 0 quit
	;
lock(var,error)
	lock @var
	quit:$quit 0 quit
	;
order(var,value,error)
	set value=$order(@var)
	quit:$quit 0 quit
	;
query(var,value,error)
	set value=$query(@var)
	quit:$quit 0 quit
	;
set(var,value,error)
	set @var=value
	quit:$quit 0 quit
	;
xecute(var,error)
	xecute var
	quit:$quit 0 quit
