$(".my-parking__btn").click(function() {

    if ($(".add-parking").is(":hidden")) {
    
		    $(".add-parking").slideDown("slow");
		    $(".my-parking__btn-icon").addClass("open");
        
    } else {
        $(".add-parking").hide("slow");
	    $(".my-parking__btn-icon").removeClass("open");
    
    }

});