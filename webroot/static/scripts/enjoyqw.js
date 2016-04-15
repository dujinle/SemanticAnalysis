function GetResult(){
	var intext = document.getElementById("intext");
	if(intext.value.length <= 0 ){
		alert("请输入自然语言");
		intext.focus();
		return false;
	}else if(intext.value.length >= 36){
		alert("输入的内容过长不得超过36字符");
		return false;
	}
	var sptext = document.getElementById("sptext");
	var restext  = document.getElementById("retext");
	var jdata = {
		'text':intext.value
	};
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + 'get_result',
		type:'post',
		dataType:'text',
		data:JSON.stringify(jdata),
		success:function(data){
			obj = data;
		},
		error:function(){
			alert(arguments);
		}
	});
	sptext.value = "";
	var json_obj = JSON.parse(obj);
	if(json_obj != null && json_obj.code == 0){
		result = json_obj.result;
		sptext.innerText = result.inlist;
		restext.innerText = JSON.stringify(result,null,"\t");
		return true;
	}else{
		restext.innerText = json_obj.message;
	}
}

function DealWords(type,action,vid,did){
	dcom = null;vcom = null;
	var idata = new Object();
	if(action != 'get'){
		if(did != null){
			dcom = document.getElementsByName(did);
		}
		if(vid != null){
			vcom = document.getElementById(vid);
		}
		if(vcom != null && vcom.value.length <= 0){
			vcom.focus();
			return false;
		}
		idata.value = vcom.value;
	}
	dir = null;
	if(dcom != null){
		for(var i = 0;i < dcom.length;i++){
			if(dcom[i].checked){
				dir = dcom[i].value;
				break;
			}
		}
	}
	idata.type = type;
	if(dir != null){
		idata.dir = dir;
	}
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + action,
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	if(obj != null && obj.code == 0){
		if(action == 'get'){
			y.innerText = JSON.stringify(obj.result,null,'\t');
		}else{
			y.innerText = obj.message;
		}
	}else{
		y.innerText = obj.message;
	}
	return false;
}
