var current_screen = "message";
function switchSection(name) {
    if (name != current_screen) {
        $('#' + current_screen).toggle('normal', function () {
            $('#' + name).toggle('normal', null);
            current_screen = name;
        });
    }
}
function read_pages() {

    read("groups.html", "#groups_");
    read("gips.html", "#gips_");
    read("handlers.html", "#handlers_");
    read("message.html", "#message_");

}
function read(name, target) {
    var d = new Date()
    $.ajax({
        url: name + "?" + d.getTime(),
        cache: false,
        dataType: "text",
        success: function (data) {

            $(target).html(data);
            if (name == "message.html") {
                load = true;
                message_start();
                init_select_sort();
                init_ul_sort();
                init_ul_css();
                set_option();
                init_forms();
            }
        },
        error: function () {

        }
    });
}
function enable_li_functionality(tar) {
    var $new_li = $(tar).children().last();
    $new_li.children("img").each(function () {
        $(this).click(function () {
            $(this).parent().remove();
        });
    });
    $new_li.mouseover(function () {
        $(this).addClass("MultipleSelectBox_li_over");
        $(this).children("img").show();
    });
    $new_li.mouseout(function () {
        $(this).removeClass("MultipleSelectBox_li_over");
        $(this).children("img").hide();
    });
    $(tar).multipleSelectBox();
}
function init_ul_css() {
    $(".multipleUlBox").each(function () {
        $(this).multipleSelectBox();

    });
    $(".multipleUlBox li").each(function () {
        $(this).append('<img src="../images/garbage.png" class="pull-right" style="display:none;height:14px;"/>');
        $(this).children("img").each(function () {
            $(this).click(function () {
                $(this).parent().remove();
            });
        });
        $(this).mouseover(function () {
            $(this).addClass("MultipleSelectBox_li_over");
            $(this).children("img").show();
        });
        $(this).mouseout(function () {
            $(this).removeClass("MultipleSelectBox_li_over");
            $(this).children("img").hide();
        });


    });

}
function removeSelf(tar) {
    $(tar).parent().remove();
}
function getSelection(selector) {
    var options = new Array();
    $(selector + ' option:selected').each(
            function () {
                options[options.length] = $(this).val();
            }
            );
    return options;

}
function getAll(selector) {
    var options = new Array();
    $(selector + ' li').each(
            function () {
                options[options.length] = $(this).attr("title");
            }
            );
    return options;
}
function contains(selector, value) {
    var values = getAll(selector);
    for (var i = 0; i < values.length; i++) {

        if (values[i] == value) {

            return true;
        }
    }

    return false;
}
function move(a, b) {
    var chosens = getSelection(a);
    var s = document.getElementById(b.substr(1));
    for (var i = 0; i < chosens.length; i++) {
        if (!contains(b, chosens[i])) {
            $(b).append('<li title="' + chosens[i].toString() + '"><font>' + chosens[i].toString() + '</font><img src="../images/garbage.png" class="pull-right" style="display:none;height:14px;"/></li>');
            enable_li_functionality($(b));
        }
    }
}
function init_ul_sort() {
    $("div .special_select_top").each(function () {
        var m = $(this).attr("sort-target-ul");
        if (m == "undefined" || m == null) {
            return;
        }

        sort_ul(m, $(this).attr("dir"));
        $(this).click(function () {
            var m = $(this).attr("sort-target-ul");
            if ($(this).attr("dir") == "0") {
                $(this).attr("dir", "1");
            }
            else {
                $(this).attr("dir", "0");
            }
            sort_ul(m, $(this).attr("dir"));

        });


    });
}
function sort_ul(name, dir) {

    var items = $('#' + name + ' li').get();
    if (dir == "0") {
        items.sort(function (a, b) {
            var keyA = $(a).text();
            var keyB = $(b).text();

            if (keyA > keyB) return -1;
            if (keyA < keyB) return 1;
            return 0;
        });
    }
    else {
        items.sort(function (a, b) {
            var keyA = $(a).text();
            var keyB = $(b).text();

            if (keyA < keyB) return -1;
            if (keyA > keyB) return 1;
            return 0;
        });
    }
    var ul = $('#' + name);
    $.each(items, function (i, li) {
        ul.append(li);
    });
}
function return_ul_options(tar) {

    var options = new Array();
    $("#" + tar + " li").each(function () {
        options[options.length] = $(this).attr("title").toString();
    });
    var ret = options.join("|");
    return ret;
}
function init_select_sort() {
    $("div .special_select_top").each(
            function () {
                var m = $(this).attr("sort-target");
                if (m == "undefined" || m == null) {
                    return;
                }

                $("#" + m).sortOptions();
                $(this).attr("dir", "0");
                $(this).click(function () {
                    var m = $(this).attr("sort-target");
                    if ($(this).attr("dir") == "0") {
                        $("#" + m).sortOptions(false);
                        $(this).attr("dir", "1");
                    }
                    else {
                        $("#" + m).sortOptions();
                        $(this).attr("dir", "0");
                    }

                });
            }
            );
}
function deleteOption(selector) {
    selector.remove(selector.selectedIndex);
}
var load = false;
function sortTable() {
    if (!load) {
        setTimeout('sortTable();', 200);
    }
    else {
        $("#sortTableExample").tablesorter();
        $("#notification_table").tablesorter();
        var sorting = [[4, 1]];
        var sorting2 = [[1, 1]];
        // sort on the first column 
        $("#sortTableExample").trigger("sorton", [sorting]);
        $("#notification_table").trigger("sorton", [sorting2]);
    }
}

function message_start() {
    $("a[name='delete_']").click(function () {
        $(this).parent().parent().hide();
        //return false;
    });
    $("div[rel=popover]")
                .popover({
                    offset: 10,
                    placement: 'below'
                })
                .click(function (e) {
                    e.preventDefault()
                });
}
function switch_priority(m) {
    var k = $('#' + m).text();
    k.trim();
    if (k == "0Low") {
        $('#' + m).attr("class", "label warning");
        $('#' + m).html("<font style='display:none;'>1</font>Medium");
    }
    else if (k == "1Medium") {
        $('#' + m).attr("class", "label important");
        $('#' + m).html("<font style='display:none;'>2</font>High");
    }
    else if (k == "2High") {
        $('#' + m).attr("class", "label");
        $('#' + m).html("<font style='display:none;'>0</font>Low");
    }
    else {
        alert(k);
    }
    $("#sortTableExample").trigger("update");
}
function show_(tar) {
    if ($(tar).is(":hidden")) {
        $(tar).slideToggle('fast');
    }
}
function switch_phone_area(tar, self) {
    if ($(self).attr("src") == "../images/dropdown.png") {
        show_(tar);
        $(self).attr("src", "../images/dropup.png");
    }
    else {
        hide_(tar);
        $(self).attr("src", "../images/dropdown.png");
    }
}
function test_modification(tar, selector) {
    $("#" + tar).find("button[name='submit_btn']").each(function () {
        if (!$(this).attr("disabled")) {
            var k = confirm("Are you sure that you want to abandon the changes?");
            if (!k) {
                $(selector).attr("selectedIndex", $(selector).attr("pre_select").toString());
                return false;
            }
            else {
                $(this).attr("disabled", true);
            }
        }
    });
    $(selector).attr("pre_select", $(selector).attr("selectedIndex"));
    return true;
}
function init_form(id) {


    $("#" + id).find('textarea').each(function () {

        if ($(this).attr("submit_status")) {
            return;
        }

        $(this).change(function () {
            $(this).parent().children('button[name="submit_btn"]').each(function () {
                $(this).attr("disabled", false);
            });
        });

        $(this).keydown(function () {
            $(this).parent().children('button[name="submit_btn"]').each(function () {
                $(this).attr("disabled", false);
            });
        });

    });


    $("#" + id + " :input").each(function () {

        if ($(this).attr("submit_status")) {
            return;
        }

        $(this).change(function () {
            $(this).parent().children('button[name="submit_btn"]').each(function () {
                $(this).attr("disabled", false);
            });
        });

        $(this).keydown(function () {
            $(this).parent().children('button[name="submit_btn"]').each(function () {
                $(this).attr("disabled", false);
            });
        });

    });

    if ($("#" + id).find('select').length > 0) {
        $("#" + id).find('select').each(function () {
            if ($(this).attr("submit_status")) {
                return;
            }
            $(this).change(function () {
                $(this).parent().children(".submit_btn").removeAttr("disabled");
            });

        });
    }


}
function init_forms() {
    init_form('GROUP_MODIFICATION');
    init_form('GIP_MODIFICATION');



}
function hide_(tar) {
    if (!$(tar).is(":hidden")) {
        $(tar).slideToggle('fast');
    }
}
function set_option() {
    $('option').each(
          function () {
              $(this).mouseover(function () { $(this).attr("class", "op_b"); });
              $(this).mouseout(function () { $(this).attr("class", ""); });
          }
          );
}
function search_message(keyword) {
    $('td[name="single_message"]').each(function () {
        if ($(this).html().toLowerCase().indexOf(keyword.toLowerCase()) == -1) {
            $(this).parent().hide();
        }
        else {
            $(this).parent().show();
        }
    });
}

