//===========================================
// Full Screen Mode
//===========================================

odoo.define('sh_entmate_theme.full_screen_systray', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');    
    var SystrayMenu = require('web.SystrayMenu');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    

    var FullScreenTemplate = Widget.extend({
        template: "FullScreenTemplate",
        events: {
            'click .expand_img': '_click_expand_button',
			'click .compress_img': '_click_compress_button',
        },
        init: function () {
        	 this._super.apply(this, arguments);
             var self = this;
        },

        _click_expand_button: function (ev) {
        	ev.preventDefault();
            var self = this;
            $('.expand_img').css("display","none");
            $('.compress_img').css("display","block");
            var elem = document.querySelector('body');
			  if (elem.requestFullscreen) {
			    elem.requestFullscreen();
			  } else if (elem.mozRequestFullScreen) { /* Firefox */
			    elem.mozRequestFullScreen();
			  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
			    elem.webkitRequestFullscreen();
			  } else if (elem.msRequestFullscreen) { /* IE/Edge */
			    elem.msRequestFullscreen();
			  }
        },
        _click_compress_button: function (ev) {
        	ev.preventDefault();
            var self = this;
            $('.compress_img').css("display","none");
            $('.expand_img').css("display","block");
            
            $('.expand_img').css("position","relative");
            $('.expand_img').css("top","30%");
            var elem = document.querySelector('body');
            if (document.exitFullscreen) {
				    document.exitFullscreen();
				  } else if (document.mozCancelFullScreen) { /* Firefox */
				    document.mozCancelFullScreen();
				  } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
				    document.webkitExitFullscreen();
				  } else if (document.msExitFullscreen) { /* IE/Edge */
				    document.msExitFullscreen();
				  }
        },

    });

    FullScreenTemplate.prototype.sequence = 2;
    // session.user_has_group('sh_entmate_theme.group_full_screen_mode').then(function(has_group) {
    // 	if(has_group){
    // 		 SystrayMenu.Items.push(FullScreenTemplate);
    // 	}
    // });
    rpc.query({
		model: 'res.users',
		method: 'search_read',
		fields: ['sh_enable_full_screen_mode'],
		domain: [['id', '=', session.uid]]
	}, { async: false }).then(function (data) {
		if (data) {
			_.each(data, function (user) {
				if (user.sh_enable_full_screen_mode) {
					SystrayMenu.Items.push(FullScreenTemplate);

				}
			});

		}
	});
   

   return {
	   FullScreenTemplate: FullScreenTemplate,
   };
});
//===========================================
//Quick Menu (main on off switch)
//===========================================

odoo.define('sh_web_quick_menu.quick_menu', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var SystrayMenu = require('web.SystrayMenu');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var ActionManager = require('web.ActionManager');

    var ActionManager = ActionManager.include({

        _preprocessAction: function (action, options) {
        	var self = this;
        	this._super.apply(this, arguments);
            var sh_url = window.location.href
            if (sh_url) {
                rpc.query({
                    model: 'sh.wqm.quick.menu',
                    method: 'is_quick_menu_avail_url',
                    args: ['', sh_url]
                }).then(function (rec) {
                    if (rec) {
                        $('.o_main_navbar').find('.o_menu_systray').find('.sh_bookmark').addClass('active');
    
                    }
                    else {
                        $('.o_main_navbar').find('.o_menu_systray').find('.sh_bookmark').removeClass('active');
                    }
                });
            }

	           
        	
        },
     
    });    



    var quick_menu = Widget.extend({
        template: "quick.menu",
        events: {
            dblclick: "on_click",
            'click li.sh_wqm_remove_quick_menu_cls i': 'remove_quick_menu',
            "keydown input.sh_bookmark_search": "_onSearchResultsNavigate",
        },
        _searchData: function () {
            var query = this.$("input.sh_bookmark_search").val();
          
            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'get_search_result',
                args: [[query]]
            })
                .then(function (menus) {

                    if (menus.length > 0) {
                        self.$el.find('.sh_search_result').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': menus}));
                    } else {
                        self.$el.find('.sh_search_result').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                });
            
        },

        _onSearchResultsNavigate: function (event) {

            this._search_def.reject();
            this._search_def = $.Deferred();
            setTimeout(this._search_def.resolve.bind(this._search_def), 50);
            this._search_def.done(this._searchData.bind(this));
        },


        init: function () {
            this._search_def = $.Deferred();
            this._super.apply(this, arguments);

        },
        remove_quick_menu: function (e) {
            e.stopPropagation();
            var self = this;
            var id = parseInt($(e.currentTarget).data('id'));
            if (id !== NaN) {
                rpc.query({
                    model: 'sh.wqm.quick.menu',
                    method: 'remove_quick_menu_data',
                    args: ['', id]
                }).then(function (res) {
                    if (res.id) {
                        if (window.location.href == res.sh_url) {
                            self.$el.parents().find('.sh_bookmark').removeClass('active');
                        }
                        
                        if (res.final_quick_menu_list.length > 0) {
                            if(res.final_quick_menu_list.length > 13){
                                self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': res.final_quick_menu_list }));
                            }else{
                                self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': res.final_quick_menu_list }));
                      
                            }

                        } else {
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                        }
                    }
                });
            }
            return false;
        },
        getUrlVars: function () {
            var vars = [], hash;
            var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                vars.push(hash[0]);
                vars[hash[0]] = hash[1];
            }
            return vars;
        },
        getUrl: function () {

            return window.location.href;
        },

        start: function () {
            //this.$var = this.$el.find('.sh_wqm_quick_menu_submenu_list_cls');
            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'get_quick_menu_data',
                args: ['', ['name', 'sh_url']],
            })
                .then(function (menus) {

                    if (menus.length > 0) {
                        if(menus.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': menus }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': menus }));
                  
                        }
                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                });
            return this._super();

            //return this._super();
        },
        getMenuRecord: function () {
            var action_id = $.bbq.getState().action;

            var model = $.bbq.getState().model
            if(!$.bbq.getState().model){
                model = $.bbq.getState().active_id
            }
            if ($.bbq.getState().view_type == 'form') {
                var res_id = $.bbq.getState().id
            }
            var sh_url = this.getUrl()
            return rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'set_quick_url',
                args: ['', sh_url, model, res_id, action_id]
            });
        },
        on_click: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var self = this;
            this.getMenuRecord().then(function (rec) {
                self.$el.addClass('active');
                if (rec.is_set_quick_menu) {
                    if (rec.final_quick_menu_list.length > 0) {

                        if(rec.final_quick_menu_list.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                  
                        }


                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }

                    
                } else {
                    self.$el.removeClass('active')
                    if (rec.final_quick_menu_list.length > 0) {
                        if(rec.final_quick_menu_list.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                  
                        }

                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                }
            });
            //refresh the page
            //location.reload(true);

        }
    });

    quick_menu.prototype.sequence = 3;
    // session.user_has_group('sh_backmate_theme_adv.group_quick_menu_mode').then(function (has_group) {
    //     if (has_group) {
    //         SystrayMenu.Items.push(quick_menu);
    //     }
    // });
    rpc.query({
		model: 'res.users',
		method: 'search_read',
		fields: ['sh_enable_quick_menu_mode'],
		domain: [['id', '=', session.uid]]
	}, { async: false }).then(function (data) {
		if (data) {
			_.each(data, function (user) {
				if (user.sh_enable_quick_menu_mode) {
					SystrayMenu.Items.push(quick_menu);

				}
			});

		}
	});


    //return quick_menu;
    return {
        quick_menu: quick_menu,
    };
});


