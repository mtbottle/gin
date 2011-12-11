/**
 * @preserve jQuery Multiple Select Box Plugin 0.6.0
 * 
 * http://plugins.jquery.com/project/jquerymultipleselectbox
 * http://code.google.com/p/jquerymultipleselectbox/
 * 
 * Apache License 2.0 - http://www.apache.org/licenses/LICENSE-2.0
 * 
 * @author Dreamltf
 * @date 2011/11/05
 * 
 * Depends: jquery.js
 */
(function($) {
	var PLUGIN_NAMESPACE = "MultipleSelectBox";
	var PLUGIN_STYLE_HORIZONTAL = "horizontal";
	var PLUGIN_STYLE_VERTICAL = "vertical";
	var PLUGIN_STYLE_DISABLED = "disabled";
	var PLUGIN_STYLE_SELECTED = "selected";
	var PLUGIN_STYLE_SELECTING = "selecting";
	var PLUGIN_STYLE_OPTGROUP = "optgroup";
	var PLUGIN_STYLE_OPTGROUPITEM = "optgroupitem";
	var defaultOptions = {
		maxLimit : -1,
		scrollSpeed : 20,
		isHorizontalMode : false,
		isMouseEventEnabled : true,
		isKeyEventEnabled : true,
		/* form options */
		submitFieldName : null,
		valueRendererArray : null,
		/* callback function */
		onCreate : null,
		onSelectStart : null,
		onSelectEnd : null,
		onSelectChange : null
	};

	/**
	 * Public Method
	 */
	$.extend($.fn, {
		/**
		 * Public : MultipleSelectBox
		 * 
		 * @param options
		 *            Object
		 * @return jQuery
		 */
		multipleSelectBox : function(options) {
			options = $.extend({}, defaultOptions, options);
			return this.each(function() {
				var $container = $(this);
				/* prepare className */
				$container.addClass(PLUGIN_NAMESPACE).addClass(options.isHorizontalMode ? PLUGIN_STYLE_HORIZONTAL : PLUGIN_STYLE_VERTICAL);
				/* prepare options */
				$container.data("options", options);
				/* disable text select */
				$container.css("MozUserSelect", "none").bind("selectstart", function() {
					return false;
				});
				/* destroy and recalculate */
				$container.destroyMultipleSelectBox().recalculateMultipleSelectBox();
				/* initialize */
				initializeMultipleSelectBox($container, options);
				/* callback function */
				if (options.onCreate) {
					$container.bind("onCreate", options.onCreate);
				}
				if (options.onSelectStart) {
					$container.bind("onSelectStart", options.onSelectStart);
				}
				if (options.onSelectEnd) {
					$container.bind("onSelectEnd", options.onSelectEnd);
				}
				if (options.onSelectChange) {
					$container.bind("onSelectChange", options.onSelectChange);
				}
				/* reset the field value */
				if (options.submitFieldName && $("input[name=" + options.submitFieldName + "]").length <= 0) {
					$container.after("<input type='hidden' name='" + options.submitFieldName + "' />");
				}
				/* trigger event */
				if (options.onCreate) {
					options.onCreate.apply($container[0]);
				}
			});
		},

		/**
		 * Public : Get Cached Rows
		 * 
		 * @param isReNew
		 *            boolean
		 * @param selector
		 *            String
		 * @return jQuery
		 */
		getMultipleSelectBoxCachedRows : function(isReNew, selector) {
			return this.pushStack($.map(this, function(container) {
				var $container = $(container);
				var $rows = $container.data("rows");
				if (isReNew || !$rows) {
					/* cache rows if necessary */
					$rows = $container.children();
					$container.data("rows", $rows);
				}
				if (selector) {
					$rows = $rows.filter(selector);
				}
				return $rows.get();
			}));
		},

		/**
		 * Public : Get Option Group Items
		 * 
		 * @param selector
		 *            String
		 * @return jQuery
		 */
		getMultipleSelectBoxOptGroupItems : function(selector) {
			return this.pushStack($.map(this, function(optGroupRow) {
				var $optGroupRow = $(optGroupRow);
				/* nextUntil */
				var resultArray = [];
				var $childGroupItem = $optGroupRow;
				while (($childGroupItem = $childGroupItem.next()).length > 0 && $childGroupItem.hasClass(PLUGIN_STYLE_OPTGROUPITEM)) {
					resultArray.push($childGroupItem[0]);
				}
				if (selector) {
					resultArray = $optGroupRow.pushStack(resultArray).filter(selector).get();
				}
				return resultArray;
			}));
		},

		/**
		 * Public : Get Row Index
		 * 
		 * @return int
		 */
		getMultipleSelectBoxRowIndex : function() {
			return this.data("index");
		},

		/**
		 * Public : Get Container Options
		 * 
		 * @return Object
		 */
		getMultipleSelectBoxOptions : function() {
			return this.data("options");
		},

		/**
		 * Public : Draw Range
		 * 
		 * @param startIndex
		 *            int
		 * @param currentIndex
		 *            int
		 * @param drawOption
		 *            Object
		 * @return jQuery
		 */
		drawMultipleSelectBox : function(startIndex, currentIndex, drawOption) {
			drawOption = $.extend({
				isGetPositionByCache : false,
				isSelectionOpposite : false,
				isSelectionRetained : false,
				isScrollBarFrozen : false,
				scrollIndex : -1
			}, drawOption);
			return this.each(function() {
				var $container = $(this);
				var $rows = $container.getMultipleSelectBoxCachedRows();
				var options = $container.getMultipleSelectBoxOptions();
				/* recalculate position or not */
				if (!drawOption.isGetPositionByCache) {
					$container.recalculateMultipleSelectBox(true, true);
				}
				var containerInfo = $container.data("info");
				/* remove invalid or duplicated request */
				if (startIndex < 0 || currentIndex < 0 || options.maxLimit == 0 || isRowUnselectable($rows.eq(startIndex))) {
					return this;
				}
				var minIndex = Math.min(startIndex, currentIndex);
				var maxIndex = Math.max(startIndex, currentIndex);
				/* prepare unselected or selecting array */
				var unselectedArray = [];
				var selectingArray = [];
				var selectedCount = 0;
				$rows.each(function(index) {
					var $childRow = $(this);
					$childRow.removeClass(PLUGIN_STYLE_SELECTING);
					if (!isRowUnselectable($childRow)) {
						var isRowSelected = $childRow.hasClass(PLUGIN_STYLE_SELECTED);
						if (minIndex <= index && index <= maxIndex) {
							if (isRowSelected) {
								if (drawOption.isSelectionOpposite) {
									unselectedArray.push($childRow);
								} else {
									selectedCount++;
								}
							} else {
								selectingArray.push($childRow);
							}
						} else {
							if (isRowSelected) {
								if (drawOption.isSelectionRetained) {
									selectedCount++;
								} else {
									unselectedArray.push($childRow);
								}
							}
						}
					}
				});
				var selectingArraySize = selectingArray.length;
				var unselectedArraySize = unselectedArray.length;
				/* calculate max limit */
				if (options.maxLimit > 0 && (selectingArraySize + selectedCount) > options.maxLimit) {
					return this;
				}
				/* reset all style if necessary */
				$rows.eq(currentIndex).addClass(PLUGIN_STYLE_SELECTING);
				for ( var i = 0; i < unselectedArraySize; i++) {
					unselectedArray[i].removeClass(PLUGIN_STYLE_SELECTED);
				}
				for ( var i = 0; i < selectingArraySize; i++) {
					selectingArray[i].addClass(PLUGIN_STYLE_SELECTED);
				}
				/* reset scroll bar */
				if (!drawOption.isScrollBarFrozen) {
					var isHorizontalMode = options.isHorizontalMode;
					var scrollIndex = drawOption.scrollIndex;
					var scrollPos = -1;
					if (scrollIndex >= 0) {
						var scrollToRow = containerInfo.rowInfoArray[scrollIndex];
						scrollPos = (isHorizontalMode ? scrollToRow.leftPos : scrollToRow.topPos);
					} else {
						var scrollToRow = containerInfo.rowInfoArray[currentIndex];
						if (isHorizontalMode) {
							scrollPos = (startIndex > currentIndex ? scrollToRow.leftPos : scrollToRow.rightPos - containerInfo.width);
						} else {
							scrollPos = (startIndex > currentIndex ? scrollToRow.topPos : scrollToRow.bottomPos - containerInfo.height);
						}
					}
					if (scrollPos >= 0) {
						if (isHorizontalMode) {
							$container.scrollLeft(scrollPos);
						} else {
							$container.scrollTop(scrollPos);
						}
					}
				}
				/* reset history */
				containerInfo.lastStartIndex = startIndex;
				containerInfo.lastCurrentIndex = currentIndex;
				return this;
			});
		},

		/**
		 * Public : Serialize MultipleSelectBox Array
		 * 
		 * @return Array
		 */
		serializeMultipleSelectBoxArray : function() {
			var options = this.getMultipleSelectBoxOptions();
			return $.map(this.getMultipleSelectBoxCachedRows(), function(row, index) {
				var $childRow = $(row);
				var resultValue = null;
				/* get text if necessary */
				if (!isRowUnselectable($childRow) && $childRow.hasClass(PLUGIN_STYLE_SELECTED) && (options.valueRendererArray == null || (resultValue = options.valueRendererArray[index]) == null)) {
					resultValue = $childRow.text();
				}
				return resultValue;
			});
		},

		/**
		 * Public : Yield MultipleSelectBox
		 * 
		 * @return jQuery
		 */
		yieldMultipleSelectBox : function() {
			$(document).unbind("mouseleave." + PLUGIN_NAMESPACE).unbind("mousemove." + PLUGIN_NAMESPACE);
			return this.unbind("mouseenter").unbind("mouseleave").unbind("mouseover");
		},

		/**
		 * Public : Destroy MultipleSelectBox
		 * 
		 * @return jQuery
		 */
		destroyMultipleSelectBox : function() {
			/* yield event handler */
			return this.yieldMultipleSelectBox().each(function() {
				var $container = $(this);
				/* reset event handler */
				$container.unbind("mousedown onCreate onSelectStart onSelectEnd onSelectChange");
				/* clear cache */
				var $rows = $container.data("rows");
				if ($rows) {
					$rows.unbind("dblclick").removeData("index");
				}
				$container.removeData("info").removeData("rows");
			});
		},

		/**
		 * Public : Recalculate MultipleSelectBox
		 * 
		 * @param isResetContainerInfo
		 *            boolean
		 * @param isResetRowsInfo
		 *            boolean
		 * @param isResetHistory
		 *            boolean
		 * @param isResetRowCache
		 *            boolean
		 * @return jQuery
		 */
		recalculateMultipleSelectBox : function(isResetContainerInfo, isResetRowsInfo, isResetHistory, isResetRowCache) {
			return this.each(function() {
				var $container = $(this);
				var $rows = $container.getMultipleSelectBoxCachedRows(isResetRowCache);
				var containerInfo = $container.data("info");
				if (!containerInfo) {
					isResetContainerInfo = isResetRowsInfo = isResetHistory = true;
					containerInfo = {};
					$container.data("info", containerInfo);
				}
				/* reset all row's position or data */
				if (isResetRowsInfo) {
					var rowInfoArray = [];
					var firstTopPos = -1;
					var firstLeftPost = -1;
					$rows.each(function(index) {
						var $childRow = $(this);
						var childRowOffset = $childRow.offset();
						var childRowTopPos = childRowOffset.top;
						var childRowLeftPos = childRowOffset.left;
						if (index == 0) {
							firstTopPos = childRowTopPos;
							firstLeftPost = childRowLeftPos;
						}
						childRowTopPos -= firstTopPos;
						childRowLeftPos -= firstLeftPost;

						$childRow.data("index", index);
						rowInfoArray.push({
							topPos : childRowTopPos,
							bottomPos : childRowTopPos + $childRow.outerHeight(),
							leftPos : childRowLeftPos,
							rightPos : childRowLeftPos + $childRow.outerWidth()
						});
					});
					containerInfo.rowInfoArray = rowInfoArray;
				}
				/* reset container's position or data */
				if (isResetContainerInfo) {
					var containerOffset = $container.offset();
					containerInfo.topPos = containerOffset.top;
					containerInfo.bottomPos = containerInfo.topPos + $container.outerHeight();
					containerInfo.height = $container.innerHeight();
					containerInfo.scrollHeight = this.scrollHeight;
					containerInfo.leftPos = containerOffset.left;
					containerInfo.rightPos = containerInfo.leftPos + $container.outerWidth();
					containerInfo.width = $container.innerWidth();
					containerInfo.scrollWidth = this.scrollWidth;
				}
				/* reset history data */
				if (isResetHistory) {
					containerInfo.lastStartIndex = containerInfo.lastCurrentIndex = containerInfo.prevStartIndex = containerInfo.prevCurrentIndex = -1;
				}
			});
		}
	});

	/**
	 * Private : Validate MultipleSelectBox
	 * 
	 * @return jQuery
	 */
	function validateMultipleSelectBox(e) {
		/* yield event handler */
		return $("." + PLUGIN_NAMESPACE).yieldMultipleSelectBox().each(function() {
			var $container = $(this);
			var options = $container.getMultipleSelectBoxOptions();
			var containerInfo = $container.data("info");
			/* trigger callback */
			if ($container.hasClass(PLUGIN_STYLE_SELECTING) && (options.onSelectEnd || options.onSelectChange || options.submitFieldName)) {
				var resultList = $container.serializeMultipleSelectBoxArray();
				var extraParameters = [ e, resultList, containerInfo.lastStartIndex, containerInfo.lastCurrentIndex, containerInfo.prevStartIndex, containerInfo.prevCurrentIndex ];
				if (options.onSelectEnd) {
					options.onSelectEnd.apply($container[0], extraParameters);
				}
				if (options.onSelectChange && (extraParameters[2] != extraParameters[4] || extraParameters[3] != extraParameters[5])) {
					options.onSelectChange.apply($container[0], extraParameters);
				}
				/* reset the field value */
				if (options.submitFieldName) {
					$("input[name=" + options.submitFieldName + "]").val(resultList.join());
				}
			}
			/* reset style */
			$container.removeClass(PLUGIN_STYLE_SELECTING);
			/* reset history */
			containerInfo.prevStartIndex = containerInfo.lastStartIndex;
			containerInfo.prevCurrentIndex = containerInfo.lastCurrentIndex;
		});
	}

	/**
	 * Private : Validate MultipleSelectBox
	 * 
	 * @return jQuery
	 */
	function isRowUnselectable($row) {
		return ($row == null || $row.hasClass(PLUGIN_STYLE_DISABLED) || $row.hasClass(PLUGIN_STYLE_OPTGROUP));
	}

	/**
	 * Private : Initialize MultipleSelectBox
	 * 
	 * @param $container
	 *            jQuery
	 * @param options
	 *            Object
	 * @return jQuery
	 */
	function initializeMultipleSelectBox($container, options) {
		var $rows = $container.getMultipleSelectBoxCachedRows();
		var rowSize = $rows.length;
		/* mouse event */
		var $document = $(document);
		if (options.isMouseEventEnabled) {
			/* process container event */
			$container.bind("mousedown", function(e) {
				var $startRow = $(e.target);
				if (this == $startRow[0]) {
					return;
				} else if (this != $startRow.parent()[0]) {
					$startRow = $startRow.parents("." + PLUGIN_NAMESPACE + ">*").eq(0);
				}
				var startIndex = $startRow.getMultipleSelectBoxRowIndex();
				/* trigger callback */
				if (options.onSelectStart) {
					var isSelectEnabled = options.onSelectStart.apply($container[0], [ e, startIndex ]);
					if (typeof (isSelectEnabled) == "boolean" && !isSelectEnabled) {
						return;
					}
				}
				/* recalculate container and all row's position */
				$container.recalculateMultipleSelectBox(true, true);
				var containerInfo = $container.data("info");
				var currentIndex = startIndex;
				/* prepare info for drawing */
				var isSelectionOpposite = false;
				var isSelectionRetained = false;
				if (options.isKeyEventEnabled) {
					if (e.shiftKey) {
						startIndex = containerInfo.lastStartIndex;
					} else if (e.ctrlKey) {
						isSelectionOpposite = isSelectionRetained = true;
					}
				}
				/* reset all style */
				$container.addClass(PLUGIN_STYLE_SELECTING);
				$container.drawMultipleSelectBox(startIndex, currentIndex, {
					isGetPositionByCache : true,
					isSelectionOpposite : isSelectionOpposite,
					isSelectionRetained : isSelectionRetained,
					isScrollBarFrozen : true
				});
				/* listening */
				$container.yieldMultipleSelectBox().bind("mouseenter", function() {
					$document.unbind("mousemove." + PLUGIN_NAMESPACE);
				}).bind("mouseleave", function() {
					if (options.scrollSpeed <= 0) {
						return;
					}
					var previousMouseXPos = -1;
					var previousMouseYPos = -1;
					var mouseRangeTotal = 0;
					$document.bind("mousemove." + PLUGIN_NAMESPACE, function(e1) {
						var mouseX = e1.pageX;
						var mouseY = e1.pageY;
						var scrollIndex = -1;
						var canDraw = false;
						if (options.isHorizontalMode) {
							// horizontal mode
							if (mouseX < containerInfo.leftPos) {
								if (currentIndex > 0 && (previousMouseXPos < 0 || mouseX < previousMouseXPos)) {
									mouseRangeTotal += (containerInfo.leftPos - mouseX) / 5;
									var targetPos = containerInfo.rowInfoArray[currentIndex].leftPos - (options.scrollSpeed / 20 * mouseRangeTotal);
									if (targetPos > 0) {
										for ( var i = currentIndex - 1; i >= 0; i--) {
											if (targetPos >= containerInfo.rowInfoArray[i].leftPos) {
												break;
											}
											currentIndex = i;
											mouseRangeTotal = 0;
										}
									} else {
										currentIndex = 0;
									}
									/* reset scrollIndex if necessary */
									if (startIndex <= currentIndex) {
										scrollIndex = currentIndex;
									}
									canDraw = true;
								}
							} else if (mouseX > containerInfo.rightPos) {
								if (currentIndex < rowSize - 1 && (previousMouseXPos < 0 || mouseX > previousMouseXPos)) {
									mouseRangeTotal += (mouseX - containerInfo.rightPos) / 5;
									var targetPos = containerInfo.rowInfoArray[currentIndex].rightPos + (options.scrollSpeed / 20 * mouseRangeTotal);
									if (targetPos < containerInfo.scrollWidth) {
										for ( var i = currentIndex + 1; i < rowSize; i++) {
											if (targetPos < containerInfo.rowInfoArray[i].rightPos) {
												break;
											}
											currentIndex = i;
											mouseRangeTotal = 0;
										}
									} else {
										currentIndex = rowSize - 1;
									}
									/* reset scrollIndex if necessary */
									if (startIndex >= currentIndex) {
										var scrollLeft = containerInfo.rowInfoArray[currentIndex].rightPos - containerInfo.width;
										for ( var i = currentIndex - 1; i >= 0; i--) {
											if (scrollLeft >= containerInfo.rowInfoArray[i].leftPos) {
												scrollIndex = i;
												break;
											}
										}
									}
									canDraw = true;
								}
							}
						} else {
							// vertical mode
							if (mouseY < containerInfo.topPos) {
								if (currentIndex > 0 && (previousMouseYPos < 0 || mouseY < previousMouseYPos)) {
									mouseRangeTotal += (containerInfo.topPos - mouseY) / 5;
									var targetPos = containerInfo.rowInfoArray[currentIndex].topPos - (options.scrollSpeed / 20 * mouseRangeTotal);
									if (targetPos > 0) {
										for ( var i = currentIndex - 1; i >= 0; i--) {
											if (targetPos >= containerInfo.rowInfoArray[i].topPos) {
												break;
											}
											currentIndex = i;
											mouseRangeTotal = 0;
										}
									} else {
										currentIndex = 0;
									}
									/* reset scrollIndex if necessary */
									if (startIndex <= currentIndex) {
										scrollIndex = currentIndex;
									}
									canDraw = true;
								}
							} else if (mouseY > containerInfo.bottomPos) {
								if (currentIndex < rowSize - 1 && (previousMouseYPos < 0 || mouseY > previousMouseYPos)) {
									mouseRangeTotal += (mouseY - containerInfo.bottomPos) / 5;
									var targetPos = containerInfo.rowInfoArray[currentIndex].bottomPos + (options.scrollSpeed / 20 * mouseRangeTotal);
									if (targetPos < containerInfo.scrollHeight) {
										for ( var i = currentIndex + 1; i < rowSize; i++) {
											if (targetPos < containerInfo.rowInfoArray[i].bottomPos) {
												break;
											}
											currentIndex = i;
											mouseRangeTotal = 0;
										}
									} else {
										currentIndex = rowSize - 1;
									}
									/* reset scrollIndex if necessary */
									if (startIndex >= currentIndex) {
										var scrollTop = containerInfo.rowInfoArray[currentIndex].bottomPos - containerInfo.height;
										for ( var i = currentIndex - 1; i >= 0; i--) {
											if (scrollTop >= containerInfo.rowInfoArray[i].topPos) {
												scrollIndex = i;
												break;
											}
										}
									}
									canDraw = true;
								}
							}
						}
						if (canDraw) {
							$container.drawMultipleSelectBox(startIndex, currentIndex, {
								isGetPositionByCache : true,
								isSelectionRetained : isSelectionRetained,
								scrollIndex : scrollIndex
							});
						}
						previousMouseXPos = mouseX;
						previousMouseYPos = mouseY;
					});
				}).bind("mouseover", function(e1) {
					var $childTarget = $(e1.target);
					if (this == $childTarget.parent()[0]) {
						currentIndex = $childTarget.getMultipleSelectBoxRowIndex();
						$container.drawMultipleSelectBox(startIndex, currentIndex, {
							isGetPositionByCache : true,
							isSelectionRetained : isSelectionRetained,
							isScrollBarFrozen : true
						});
					}
				});
				/* IE hacked for mouse event */
				if ($.browser.msie) {
					$document.bind("mouseleave." + PLUGIN_NAMESPACE, function() {
						$document.one("mousemove." + PLUGIN_NAMESPACE, function(e1) {
							if (!e1.button) {
								validateMultipleSelectBox(e1);
							}
						});
					});
				}
				return;
			});
			/* process row event */
			/* select group items automatically */
			$rows.filter("." + PLUGIN_STYLE_OPTGROUP).bind("dblclick", function(e) {
				var childGroupItemList = $(this).getMultipleSelectBoxOptGroupItems();
				var childGroupItemSelectSize = childGroupItemList.length;
				if (childGroupItemSelectSize > 0) {
					if (options.maxLimit > 0 && childGroupItemSelectSize > options.maxLimit) {
						childGroupItemSelectSize = options.maxLimit;
					}
					$container.drawMultipleSelectBox(childGroupItemList.eq(0).getMultipleSelectBoxRowIndex(), childGroupItemList.eq(childGroupItemSelectSize - 1).getMultipleSelectBoxRowIndex(), {
						isScrollBarFrozen : true
					});
					/* special case */
					$container.addClass(PLUGIN_STYLE_SELECTING);
					validateMultipleSelectBox(e);
				}
			});
		}
		return $container;
	}

	/**
	 * Event Control
	 */
	$(document).bind("mouseup." + PLUGIN_NAMESPACE, function(e) {
		validateMultipleSelectBox(e);
	});
})(jQuery);