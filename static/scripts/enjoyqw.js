function Add_Split_Word(){

	var x = document.getElementById("aspwid");
	if(x.value == ""){
		alert("请输入词组");
		x.focus();
		return false;
	}
	idata = {"word":x.value};
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + "add_word",
		type:"post",
		dataType:"text",
		data:JSON.stringify(idata),
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	var st = document.getElementById("status_id");
	if(obj != null){
		st.innerHTML = obj.message;
	}
	return false;
}

function Del_Split_Word(){

	var x = document.getElementById("spwid");
	if(x.value.length <= 0){
		x.focus();
		return false;
	}
	var obj = null;
	idata = {"word":x.value};
	$.ajax({
		async:false,
		url: $basepath + "del_word",
		type:"post",
		dataType:"text",
		data:JSON.stringify(idata),
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	var y = document.getElementById("status_id");
	if(obj != null){
		y.innerHTML = obj.message;
	}
	return false;
}

function Get_Result(){
		var str= document.getElementById("rawtext").value;
		if(str.length <= 0 ){
			alert("请输入自然语言");
			document.getElementById("rawtext").focus();
			return false;
		}else if(str.length >= 36){
			alert("输入的内容过长不得超过36字符");
			return false;
		}
		var sptext = document.getElementById("spid");
		var restext  = document.getElementById("resid");
		var jdata = {
			'text':str
		};
		var obj = null;
		$.ajax({
			async:false,
			url: $basepath,
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
		if(json_obj != null && json_obj.code != null){
			result = json_obj.result;
			sptext.value = result.inlist;
			restext.value = JSON.stringify(result,null,"\t");
			return true;
		}else{
			var x = document.getElementById("status_id");
			x.innerHTML = "没有语义结果返回";
		}
	}

function submit(){
		var form = document.getElementById("fid");
		var x = document.getElementById("rawtext");
		if(x.value.length <= 0){
			alert("请输入数据");
			x.fource();
			return false;
		}
		form.submit();
		alert("数据提交成功");
		location.reload();
		return false;
	}

function Get_Scene(){
		var sid = document.getElementById("sceneid");
		var obj = null;
		if(sid.value.length <= 0){
			alert("请选择同义词");
			sid.focus();
			return false;
		}
		idata = {"scene":sid.value};
		$.ajax({
			async:false,
			url: $basepath + "get_scene",
			type:"post",
			dataType:"text",
			data:JSON.stringify(idata),
			success:function(data){ obj = data;}
		});
		var json_obj = JSON.parse(obj);
		y = document.getElementById('status_id');
		if(json_obj.code == -1){
			y.innerHTML = json_obj.message;
			return false;
		}
		y.innerHTML = json_obj.message;
		swid = document.getElementById('sdimen_id');
		swid.value = JSON.stringify(json_obj.result,null,' ');
		return true;
}

function Reg_Scene(){
		var sid = document.getElementById("sceneid");
		var wid = document.getElementById("wordid");
		var obj = null;
		if(sid.value.length <= 0){
			alert("请选择同义词");
			sid.focus();
			return false;
		}
		if(wid.value.length <= 0){
			alert("请输入关键字");
			wid.focus();
			return false;
		}
		idata = {
			"scene":sid.value,
			"word":wid.value
		};
		$.ajax({
			async:false,
			url: $basepath + "reg_scene",
			type:"post",
			dataType:"text",
			data:JSON.stringify(idata),
			success:function(data){ obj = data;}
		});
		var json_obj = JSON.parse(obj);
		y = document.getElementById('status_id');
		if(json_obj.code == -1){
			y.innerHTML = json_obj.message;
			return false;
		}
		y.innerHTML = json_obj.message;
		return true;
}

function Del_Scene(){
	var sid = document.getElementById("sceneid");
	var wid = document.getElementById("wordid");
	var obj = null;
	if(sid.value.length <= 0){
		sid.focus();
		return false;
	}
	if(wid.value.length <= 0){
		wid.focus();
		return false;
	}
	idata = {
		"scene":sid.value,
		"word":wid.value
	};
	$.ajax({
		async:false,
		url: $basepath + "del_scene",
		type:"post",
		dataType:"text",
		data:JSON.stringify(idata),
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	if(obj != null){
		y = document.getElementById('status_id');
		y.innerHTML = obj.message;
	}
	return false;
}

function Get_Dimen(){
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + "get_dimen",
		type:"post",
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	if(obj.code == -1){
		y.innerHTML = obj.message;
		return false;
	}
	y.innerHTML = obj.message;
	swid = document.getElementById('sdimen_id');
	swid.value = JSON.stringify(obj.result,null,'\t');
	return true;
}

function Reg_Dimen(){
	var sid = document.getElementById("wdimenid");
	var wid = document.getElementById("kdimenid");
	var obj = null;
	if(sid.value.length <= 0){
		sid.focus();
		return false;
	}
	if(wid.value.length <= 0){
		wid.focus();
		return false;
	}
	idata = {
		"word":sid.value,
		"label":wid.value
	};
	$.ajax({
		async:false,
		url: $basepath + "reg_dimen",
		type:"post",
		dataType:"text",
		data:JSON.stringify(idata),
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.innerHTML = obj.message;
	return false;
}

function Check_Dimen(){
	var sid = document.getElementById("spdid");
	var obj = null;
	if(sid.value.length <= 0){
		sid.focus();
		return false;
	}
	idata = {
		"word":sid.value,
	};
	$.ajax({
		async:false,
		url: $basepath + "check_dimen",
		type:"post",
		dataType:"text",
		data:JSON.stringify(idata),
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	swid = document.getElementById('sdimen_id');
	if(obj.code == 0){
		swid.value = JSON.stringify(obj.result,null,'\t');
	}
	y = document.getElementById('status_id');
	y.innerHTML = obj.message;
	return false;
}

function Get_Model(){
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + "get_model",
		type:"post",
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	swid = document.getElementById('sdimen_id');
	if(obj.code == 0){
		swid.value = JSON.stringify(obj.result,null,'\t');
	}
	y = document.getElementById('status_id');
	y.innerHTML = obj.message;
	return false;
}

function Reg_Regs(){
	spword = document.getElementById("spdid");
	if(spword.value.length <= 0){
		spword.focus();
		return false;
	}
	levels = document.getElementsByName("level");
	qufan = document.getElementById("qufanid");
	ldata = levels[0].value;
	for(var i = 0;i < levels.length;i++){
		if(levels[i].checked){
			ldata = levels[i].value;
			break;
		}
	}
	if(qufan.checked == true){
		ldata = "!" + ldata;
	}
	idata = {
		"word":spword.value,
		"level":ldata
	};
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + "reg_regs",
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.innerHTML = obj.message;
	return false;
}

function Reg_Quant(){

	fword = document.getElementById("twordid");
	dirs = document.getElementsByName("dir");
	if(fword.value.length <= 0){
		fword.focus();
		return false;
	}
	dir = dirs[0].value;
	for(var i = 0;i < dirs.length;i++){
		if(dirs[i].checked){
			dir = dirs[i].value;
			break;
		}
	}
	idata = {
		"word":fword.value,
		"dir":dir
	};
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + "reg_quant",
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.innerHTML = obj.message;
	return false;
}
