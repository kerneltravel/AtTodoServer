
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `todo`;
CREATE TABLE `todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `content` char(100) NOT NULL COMMENT '内容',
  `create_date` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `sort_s` int(11) NOT NULL DEFAULT '0' COMMENT '辅助排序',
  `remind` int(11) DEFAULT '0' COMMENT '是否提醒',
  `finish` int(11) DEFAULT '0' COMMENT '是否完成，完成后记录完成时间',
  `remove` int(11) DEFAULT '0' COMMENT '是否被删除了',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` char(60) NOT NULL COMMENT '邮箱',
  `psw` char(64) NOT NULL COMMENT '密码',
  `username` char(20) NOT NULL COMMENT '用户名字',
  `ssid` char(64) DEFAULT NULL COMMENT 'SSID用户识别用户身份',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

