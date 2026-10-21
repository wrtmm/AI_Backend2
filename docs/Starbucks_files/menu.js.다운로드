$(document).ready(function(){

	// 제품 마우스 오버시 커버
	/*
	$("div.product_list > dl > dd > ul > li").bind("mouseover focusin", function(){ // 키보드 접근성을 위해 focusin 으로 이벤트 처리
		$(this).append("<div class='product_list_cover'></div>");
		$(this).find('a').children('img').stop().animate({"transform": "scale(1.2, 1.2)"});
		
	});
	*/
	/*
	$("div.product_list > dl > dd > ul > li").bind("mouseleave focusout", function(){ // 키보드 접근성을 위해 focusout 으로 이벤트 처리
		$("div.product_list_cover").remove();
		$("div.product_list > dl > dd > ul > li").find('a').children('img').stop(true, true).animate({"transform": "scale(1, 1)"});
	});
	*/
	
	$("div.product_list > dl > dd > ul > li").bind("click", function(){
		goUrl = $(this).find("a").attr("href");
		location.href = goUrl ;
	});

	var $viewBtn = true;
	$(".productView").bind("click", function(){
		if($viewBtn == true){
			$(".productListArea").slideDown('normal', function(){
				$(".productMore").show();
			});
			$(this).find("img").attr("src", $(this).find("img").attr("src").replace("_down.png","_up.png"));
			$viewBtn = false;
		}else{
			$(".productListArea").slideUp('normal', function(){
				$(".productMore").hide();
			});
			$(this).find("img").attr("src", $(this).find("img").attr("src").replace("_up.png","_down.png"));
			$viewBtn = true;
		}
	});

	$(".productMore").bind("click", function(){
		$(".productListArea ul").append( productAdd );
	});

	var productAdd = 
	'<li><dl><dt><a href="javascript:void(0)"><img src="/common/img/menu/product1.jpg" alt="" /></a></dt><dd>허니 바닐라 마키야또</dd></dl></li>' +
	'<li><dl><dt><a href="javascript:void(0)"><img src="/common/img/menu/product2.jpg" alt="" /></a></dt><dd>헤이즐넛 마키아또</dd></dl></li>' +
	'<li><dl><dt><a href="javascript:void(0)"><img src="/common/img/menu/product3.jpg" alt="" /></a></dt><dd>부드러운 생크림 카스텔라</dd></dl></li>' +
	'<li><dl><dt><a href="javascript:void(0)"><img src="/common/img/menu/product4.jpg" alt="" /></a></dt><dd>메이플 피칸 데니쉬 롤</dd></dl></li>';

	// 분류 보기 위 & 아래 버튼
	var btnActive = false;
	$("div.product_kind_btn").bind("click", function(){
		if( btnActive == false ){
			$(this).find("img").attr("src", $(this).find("img").attr("src").replace("up", "down")).attr("alt","분류보기 메뉴 펼치기"); // 접근성_20171123 alt 값 추가
			$("div.product_toggle_wrap").hide();
			btnActive = true;
		}else{
			$(this).find("img").attr("src", $(this).find("img").attr("src").replace("down", "up")).attr("alt", "분류보기 메뉴 접기"); // 접근성_20171123 alt 값 추가
			$("div.product_toggle_wrap").show();
			btnActive = false;
		}
	});

	// 분류 보기 - 카테고리 별 & 서비스 별
	$("dl.product_kind_tab > dt > a:not(.selected)").parent().next().hide();
	$("dl.product_kind_tab > dt > a").bind("click", function(){
		$("dl.product_kind_tab > dt > a").removeClass("selected");
		$(this).addClass("selected");
		$("dl.product_kind_tab > dd").hide();
		$(this).parent().next().show();
		return false;
	});
	$("dl.product_kind_tab > dt.dt1 > a").bind("click", function(){
		$(".product_result_wrap01").show();
		$(".product_result_wrap02").hide();
	});
	$("dl.product_kind_tab > dt.dt2 > a").bind("click", function(){
		$(".product_result_wrap02").show();
		$(".product_result_wrap01").hide();
	});

	// 음료 - 카테고리 별 - 사진으로 보기 & 영양정보로 보기
	$("dl.product_view_tab01 > dt > a:not(.selected)").parent().next().hide();
	$("dl.product_view_tab01 > dt > a").bind("click", function(){
		
		if($(this).hasClass('a2')) {
			$('#mn_select_wrap').hide();
		} else {
			$('#mn_select_wrap').show();
		}
		
		$("dl.product_view_tab01 > dt > a").removeClass("selected");
		$(this).addClass("selected");
		$("dl.product_view_tab01 > dd").hide();
		$(this).parent().next().show();
		return false;
	});

	// 음료 - 서비스 별 - 사진으로 보기 & 영양정보로 보기
	$("dl.product_view_tab02 > dt > a:not(.selected)").parent().next().hide();
	$("dl.product_view_tab02 > dt > a").bind("click", function(){
		$("dl.product_view_tab02 > dt > a").removeClass("selected");
		$(this).addClass("selected");
		$("dl.product_view_tab02 > dd").hide();
		$(this).parent().next().show();
		return false;
	});

	$('div.more_wrap').bind('click', function(){
		var warning = $('div.product_w_txt').css('height');
		if(warning == '266px'){
			$('div.product_w_txt').css({'height':'auto'});
			$(this).find('a').html('닫기&nbsp;&nbsp;&nbsp;<img src="/common/img/menu/more_arrow_up.jpg" alt="더보기 버튼">');
		}else{
			$('div.product_w_txt').css({'height':'266px'});
			$(this).find('a').html('더보기&nbsp;&nbsp;&nbsp;<img src="/common/img/menu/more_arrow_down.jpg" alt="닫기 버튼">');
		}
	});

});