/**
 * Created by liyongjiang on 2016/5/24.
 */
//这些是测试函数
function analyse() {
    alert("analyse");
}
//这个是CT函数
function add_ct() {
	ct_obj = document.getElementById('ct_text');
	ct_value = ct_obj.value;

	idata = new Object();
	idata.type = 'CT';
	idata.mdl = $mdl;
	idata.value = ct_value;

	$.ajax({
		async:false,
		url: $basepath + 'add',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}
//这个是删除数据
function del(type,vid) {
	v_obj = document.getElementById(vid);
	v_value = v_obj.value;

	idata = new Object();
	idata.type = type;
	idata.value = v_value;
	idata.mdl = $mdl;

	$.ajax({
		async:false,
		url: $basepath + 'del',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}
//这个是MO函数
function add_sg() {
	sg_obj = document.getElementById('sg_text');
	sg_value = sg_obj.value;

	idata = new Object();
	idata.type = 'SG';
	idata.mdl = $mdl;
	idata.value = sg_value;

	$.ajax({
		async:false,
		url: $basepath + 'add',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}
//这个是获取数据
function get(type) {
	idata = new Object();
	idata.type = type;
	idata.mdl = $mdl;

	$.ajax({
		async:false,
		url: $basepath + 'get',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	if(obj != null && obj.code == 0){
		y.value = JSON.stringify(obj.result,null,' ');
	}else{
		y.value = obj.message.replace(/#/g,'\n');
	}
}

//这个是功能描述的函数
function describe( dum) {
    if (dum == "ct-describe") {
        document.getElementById("status_id").value = "餐饮分类:对餐饮的风格的分类，如火锅店、川菜、日本料理、饺子等"
    }
}
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
	sptext.innerText = null;
	restext.innerText = null;
	var jdata = {
		'text':intext.value,
		'mdl':$mdl
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
		sptext.value = result.inlist;
		restext.value = JSON.stringify(result,null," ");
		return true;
	}else{
		restext.value = json_obj.message.replace(/#/g,'\n');
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
	idata.mdl = $mdl;
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
			y.value = JSON.stringify(obj.result,null,' ');
		}else{
			y.value = obj.message.replace(/#/g,'\n');
		}
	}else{
		y.innerText = obj.message.replace(/#/g,'\n');
	}
	return false;
}

function save_data(mdl){
	var obj = null;
	data = {
		'mdl':mdl
	};
	$.ajax({
		async:false,
		url: $basepath + 'save_data',
		type:'post',
		dataType:"text",
		data:JSON.stringify(data),
		success:function(data){
			obj = data;
		},
		error:function(){
			alert(arguments);
		}
	});
	sptext.value = "";
	var json_obj = JSON.parse(obj);
	y = document.getElementById('status_id');
	y.value = json_obj.message.replace(/#/g,'\n');
}
