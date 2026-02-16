$(document).ready(function () {
    
    // open modal per item
    $(document).on("click", ".product_group", function () {
        
        let id = $(this).attr("data-id");

        $("#product_id").val(id);
        $("#openQuantityModal").click();
        
    });

    // add item to cart
    $("#addQuantityForm").submit(function (e) { 
        e.preventDefault();

        var xhref = $.ajax({
            type: "post",
            url: location.href,
            data: $(this).serialize(),
            
            success: function (response) {

                if (response.success) {
                    console.log(response)
                    $("#cart").load(location.href+" #cart>*","");
                    $("#ConfirmationForm").load(location.href+" #ConfirmationForm>*","");
                    $("#dialogDeleteClose").click();
                    $("#qtty").val("");
                } else {
                    alert(response.err)
                }
                
            }
        });

        
    });

    // delete item
    $(document).on("click", ".delbtn", function () {
        
        let itemID = $(this).attr("data-id");
        
        console.log(itemID)
        // $("#total").text( $("#subtotaltxt").text() );

        $("#delItem").attr("href", itemID);

        $("#opendialogDelete").click();

    });

    $("#delItem").click( function(e) {
        e.preventDefault();

        window.location.href = $(this).attr('href');
        
        
    });


    $(document).on("click", "#proceedBtn", function (e) { 
        // $("#total").text( $(document).find("#subtotaltxt").text() );
        $("#openConfirmationModal").click();
        
    });

    // show hide the payment form depending on radio button value

    $('input:radio[name="payment_method"]').change(function () { 
        
        let payment_method = $(this).val();

        if (payment_method == "cash") {
            $("#cash_form").show();
            $("#gcash_form").hide();
        } else if (payment_method == "gcash") {
            $("#gcash_form").show();
            $("#cash_form").hide();
        } else {
            $("#cash_form").hide();
            $("#gcash_form").hide();
        }


    });

    // show change when typing
    var total = parseInt($("#grand_total").attr("data-subtotal"));

    const change_func = (payment, total) => {
        return parseInt(payment) - total
    }

    

    $(document).on("keyup", "#payment", function () { 
    
        let payment = $(this).val()
        let change = change_func(payment, total)

        console.log(payment)

        let formatted_change = (Math.round(change * 100) / 100).toFixed(2);

        if(payment >= total) {
            $("#payment_change").val("₱ " + formatted_change);
            //console.log("₱ " + formatted_change)
            $("#cash_btn").removeAttr("disabled");
        } else {
            $("#payment_change").val("₱ " + "0.00");
            $("#cash_btn").attr("disabled", "disabled");
        }
        
        //console.log($(this).val())
    });


});