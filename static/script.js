$(".clients__icon").click(function() {

    if ($(".drop-down__text--clients").is(":hidden")) {
    
		    $(".drop-down__text--clients").slideDown("slow");
		    $(".clients__icon").addClass("open");
        
    } else {
        $(".drop-down__text--clients").hide("slow");
	    $(".clients__icon").removeClass("open");
    
    }

});

$(".owners__icon").click(function() {

    if ($(".owners__wrap").is(":hidden")) {
    
		    $(".owners__wrap").slideDown("slow");
		    $(".owners__icon").addClass("open");
        
    } else {
        $(".owners__wrap").hide("slow");
	    $(".owners__icon").removeClass("open");
    
    }

});

$(".free-spots").click(function() {
    if ($(event.target).is(".parking-spot"))  {
        if (!($(event.target).is(".is-taken")))  {
            $(".parking-spot").removeClass("chosen");
            $(event.target).addClass("chosen");
            $(".book").removeClass("is-hidden");
        }
    }
})