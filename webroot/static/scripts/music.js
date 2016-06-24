/**
 * Created by liyongjiang on 2016/5/24.
 */
//这些是测试函数
function analyse() {
    alert("analyse");
}
//这个是MS函数
function add_ms() {
	ms_obj = document.getElementById('ms_text');
	ms_value = ms_obj.value;

	idata = new Object();
	idata.type = 'MS';
	idata.mdl = $mdl;
	idata.value = ms_value;

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
//这个是MT函数
function add_mt() {
	mt_obj = document.getElementById('mt_text');
	mt_value = mt_obj.value;

	idata = new Object();
	idata.type = 'MT';
	idata.mdl = $mdl;
	idata.value = mt_value;

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
//这个是ML函数
function add_ml() {
	ml_obj = document.getElementById('ml_text');
	ml_value = ml_obj.value;

	idata = new Object();
	idata.type = 'ML';
	idata.mdl = $mdl;
	idata.value = ml_value;

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
//这个是MO函数
function add_mo() {
	mo_obj = document.getElementById('mo_text');
	mo_value = mo_obj.value;

	idata = new Object();
	idata.type = 'MO';
	idata.mdl = $mdl;
	idata.value = mo_value;

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
    if (dum == "ms-describe") {
        document.getElementById("status_id").value = "音乐风格:对音乐的风格的分类，如DJ、串烧、摇滚等"
    }
    else if (dum == "mt-describe") {
        document.getElementById("status_id").value = "音乐类型：对音乐类型的分类，如纯音乐、钢琴曲、伴奏等"
    }
    else if (dum == "ml-describe") {
        document.getElementById("status_id").value = "音乐语种：对音乐语种的分类，如汉语、粤语、欧美、日韩等"
    }
	else if (dum == "sg-describe") {
		document.getElementById("status_id").value = "音乐歌手：对音乐歌手的名字，如刘德华、孙燕姿、后街男孩、wonder girls等"
	}
    else if (dum == "mo-describe") {
        document.getElementById("status_id").value = "音乐其他：音乐其他的分类，如排行、榜单、最流行等"
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
