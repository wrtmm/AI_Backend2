$(document).ready(function () {
  $.menuProduct = {
    tmplete1: function () {
      var tmplete = "";

      tmplete = tmplete + '<li>';
      tmplete = tmplete + '<dl>';
      tmplete = tmplete + '<dt><a href="javascript:void(0);" class="jy_listAttr" tmpAttr="${$item.product_CD()}" tmpCate="${$item.f_CATE_CD()}"><img alt="${$item.product_NM()}" src="${$item.file_PATH().replace("www", "image")}"></a></dt>'; // 접근성_20171201 alt 추가
      tmplete = tmplete + '<dd>${$item.product_NM()}</dd>';
      tmplete = tmplete + '</dl>';
      tmplete = tmplete + '</li>';

      $.template("productTmp", tmplete);
    }
    ,
    getList: function (tmp_cate, x) {
			/*
			var param = {
					//menu_cd : menu_cd,
			};
			 */
            var option = {
                    'CATE_CD' : tmp_cate
            };
            
			//__ajaxCall("/menu/getProductMainListAjax.do", param, true, "json", "post",
            __ajaxCall('/menu/getProductMainListAjax.do', option , true, "JSON", "POST", 
			
				function(data){

					$.tmpl( "productTmp", data.list , {
						file_PATH : function(){
							var file_PATH = this.data.file_PATH;
							return this.data.img_UPLOAD_PATH + file_PATH;
						},
						product_NM : function(){
							var product_NM = this.data.product_NM;
							return product_NM;
						},
						product_CD : function(){
							var product_CD = this.data.product_CD;
							return product_CD;
						},
						f_CATE_CD : function(){
							var f_CATE_CD = this.data.f_CATE_CD;
							return f_CATE_CD;
						}
				
					}).appendTo($(".productList").eq(x).find('ul'));
					
					$.tmpl( "productTmp", data.list , {
						file_PATH : function(){
							var file_PATH = this.data.file_PATH;
							return this.data.img_UPLOAD_PATH + file_PATH;
						},
						product_NM : function(){
							var product_NM = this.data.product_NM;
							return product_NM;
						},
						product_CD : function(){
							var product_CD = this.data.product_CD;
							return product_CD;
						},
						f_CATE_CD : function(){
							var f_CATE_CD = this.data.f_CATE_CD;
							return f_CATE_CD;
						}
				
					}).appendTo($(".m_productList").eq(x).find('ul'));
					
					
					$('.jy_listAttr').bind('click', function() {
						tmp_seq = $(this).attr('tmpAttr');
						tmp_cate = $(this).attr('tmpCate');
						if(tmp_seq != "") {
							pageView(tmp_seq, tmp_cate);
						}
					});
					
					/*
					if($( "#productList").html() == "") {
						$("#productMore").hide();
					} else {
						$("#productMore").show();
					}
					*/
					$("#productMore").hide();
					
				}
				,function(data){
				
				});
		}
	}
	
	$.menuProduct.tmplete1();
	//$.menuProduct.getList();
	/*
	$.menuProduct.getList('W0000065');
	$.menuProduct.getList('W0000066');
	$.menuProduct.getList('W0000114');
	*/
});


function pageView(pro_cd, f_cate_cd) {
  //form
  var form = document.createElement("form");
  form.setAttribute("method", "post");
  if (f_cate_cd == "W0000001") {
    form.setAttribute("action", "/menu/drink_view.do");
  } else if (f_cate_cd == "W0000012") {
    form.setAttribute("action", "/menu/food_view.do");
  } else if (f_cate_cd == "W0000022") {
    form.setAttribute("action", "/menu/product_view.do");
  }
  document.body.appendChild(form);
  //input
  var product_cd = document.createElement("input");
  product_cd.setAttribute("type", "hidden");
  product_cd.setAttribute("name", "product_cd");
  product_cd.setAttribute("id", "product_cd");
  product_cd.setAttribute("value", pro_cd);
  form.appendChild(product_cd);

  //폼전송
  form.submit();
}
