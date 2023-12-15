setTimeout(function(){
	$("#website_cookies_bar .modal").fadeIn();
	console.log('set timer')
},1000);

function GetLocalValue() {
	$("#website_cookies_bar .modal").addClass("d-none");
	localStorage.setItem("class", "d-none");
}

function CloseModal() {
	$("#website_cookies_bar .modal").addClass(localStorage.getItem("class"));
}

$(function() {
    CloseModal();
});