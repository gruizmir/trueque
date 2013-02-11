CREATE SCHEMA trueque;

CREATE TABLE trueque.`Country` ( 
	`ID_country`         INT  NOT NULL  AUTO_INCREMENT,
	`Country_name`       VARCHAR( 20 )  NOT NULL  ,
	CONSTRAINT pk_country PRIMARY KEY ( `ID_country` )
 );

CREATE TABLE trueque.`City` ( 
	`ID_city`            INT  NOT NULL  ,
	`ID_country`         INT  NOT NULL  ,
	`City_name`          VARCHAR( 20 )  NOT NULL  ,
	CONSTRAINT pk_city PRIMARY KEY ( `ID_city` )
 );

CREATE INDEX ID_country ON trueque.`City` ( `ID_country` );

CREATE TABLE trueque.`Usuario` ( 
	`ID_usuario`         INT  NOT NULL  AUTO_INCREMENT,
	`Usuario_password`   VARCHAR( 25 )  NOT NULL  ,
	`Usuario_name`       VARCHAR( 20 )  NOT NULL  ,
	`Usuario_lastname`   VARCHAR( 20 )  NOT NULL  ,
	`Usuario_bullletins` BIT  NOT NULL  ,
	`Usuario_email_1`    VARCHAR( 30 )  NOT NULL  ,
	`Usuario_email_2`    VARCHAR( 30 )    ,
	`Usuario_phone_1`    VARCHAR( 10 )    ,
	`Usuario_phone_2`    VARCHAR( 10 )    ,
	`Usuario_language`   VARCHAR( 5 )    ,
	`Usuario_FB_Token`   VARCHAR( 150 )    ,
	`Usuario_TW_Token`   VARCHAR( 160 )    ,
	`Usuario_register_date` DATETIME  NOT NULL  ,
	`Usuario_city`       INT    ,
	`Usuario_level`      INT  NOT NULL  ,
	`Usuario_rating`     INT  NOT NULL  ,
	`Usuario_ranking_qty` INT    ,
	`Usuario_quds`       INT  NOT NULL  ,
	`Usuario_follower_qty` INT  NOT NULL  ,
	`Usuario_followe_qty` INT  NOT NULL  ,
	`Usuario_barter_qty` INT  NOT NULL  ,
	`Usuario_remaining_invitations` INT  NOT NULL  ,
	`Usuario_art`        BIT  NOT NULL  ,
	`Usuario_music`      BIT  NOT NULL  ,
	`Usuario_tech`       BIT  NOT NULL  ,
	`Usuario_cars`       BIT  NOT NULL  ,
	`Usuario_travels`    BIT  NOT NULL  ,
	`Usuario_clothes`    BIT  NOT NULL  ,
	`Usuario_cine`       BIT  NOT NULL  ,
	`Use_sports`         BIT  NOT NULL  ,
	`Usuario_eco`        BIT  NOT NULL  ,
	`Usuario_culture`    BIT  NOT NULL  ,
	`Usuario_spectacles` BIT  NOT NULL  ,
	`Usuario_love`       BIT  NOT NULL  ,
	`Usuario_food`       BIT  NOT NULL  ,
	`Usuario_vacations`  BIT  NOT NULL  ,
	`Usuario_services`   BIT  NOT NULL  ,
	CONSTRAINT pk_usuario PRIMARY KEY ( `ID_usuario` )
 );

CREATE INDEX Usuario_city ON trueque.`Usuario` ( `Usuario_city` );

CREATE TABLE trueque.`Rating` ( 
	`ID_rating`          INT  NOT NULL  AUTO_INCREMENT,
	`ID_rater`           INT    ,
	`ID_rated`           INT  NOT NULL  ,
	`Rating_level`       INT  NOT NULL  ,
	`Rating_datetime`    DATETIME  NOT NULL  ,
	CONSTRAINT pk_rating PRIMARY KEY ( `ID_rating` )
 );

CREATE INDEX ID_rater ON trueque.`Rating` ( `ID_rater` );

CREATE INDEX ID_rated ON trueque.`Rating` ( `ID_rated` );

CREATE TABLE trueque.`Followers` ( 
	`ID_follower`        INT  NOT NULL  ,
	`ID_followed`        INT  NOT NULL  ,
	CONSTRAINT pk_followers PRIMARY KEY ( `ID_follower`, `ID_followed` )
 );

CREATE INDEX ID_followed ON trueque.`Followers` ( `ID_followed` );

CREATE TABLE trueque.`WarningReason` ( 
	`ID_reason`          INT  NOT NULL  AUTO_INCREMENT,
	`Reason_text`        VARCHAR( 50 )  NOT NULL  ,
	CONSTRAINT pk_warningreason PRIMARY KEY ( `ID_reason` )
 );

CREATE TABLE trueque.`Warning` ( 
	`ID_warning`         INT  NOT NULL  AUTO_INCREMENT,
	`ID_sender`          INT  NOT NULL  ,
	`ID_receiver`        INT  NOT NULL  ,
	`Warning_reason`     INT    ,
	`Warning_message`    TEXT  NOT NULL  ,
	`Warning_datetime`   INT  NOT NULL  ,
	CONSTRAINT pk_warning PRIMARY KEY ( `ID_warning` )
 );

CREATE INDEX ID_sender ON trueque.`Warning` ( `ID_sender` );

CREATE INDEX ID_receiver ON trueque.`Warning` ( `ID_receiver` );

CREATE INDEX Warning_reason ON trueque.`Warning` ( `Warning_reason` );

CREATE TABLE trueque.`Category` ( 
	`ID_category`        INT  NOT NULL  AUTO_INCREMENT,
	`Category_name`      VARCHAR( 20 )  NOT NULL  ,
	CONSTRAINT pk_category PRIMARY KEY ( `ID_category` )
 );

CREATE TABLE trueque.`Product` ( 
	`ID_product`         INT  NOT NULL  AUTO_INCREMENT,
	`ID_owner`           INT  NOT NULL  ,
	`Product_name`       VARCHAR( 30 )  NOT NULL  ,
	`Product_img`        VARCHAR( 100 )  NOT NULL  ,
	`Product_description` TEXT    ,
	`Product_Q_amount`   INT  NOT NULL  ,
	`Product_datetime`   DATETIME  NOT NULL  ,
	`Product_follower_qty` INT  NOT NULL  ,
	`Product_visit_qty`  INT  NOT NULL  ,
	`Product_country`    VARCHAR( 20 )  NOT NULL  ,
	`Product_city`       VARCHAR( 20 )  NOT NULL  ,
	CONSTRAINT pk_product PRIMARY KEY ( `ID_product` )
 );

CREATE INDEX ID_owner ON trueque.`Product` ( `ID_owner` );

CREATE TABLE trueque.`Product_category` ( 
	`ID_product`         INT  NOT NULL  ,
	`ID_category`        INT  NOT NULL  ,
	CONSTRAINT pk_product_category PRIMARY KEY ( `ID_product`, `ID_category` )
 );

CREATE INDEX ID_category ON trueque.`Product_category` ( `ID_category` );

CREATE TABLE trueque.`Product_follower` ( 
	`ID_product`         INT  NOT NULL  ,
	`ID_user`            INT  NOT NULL  ,
	CONSTRAINT pk_product_follower PRIMARY KEY ( `ID_product`, `ID_user` )
 );

CREATE INDEX ID_user ON trueque.`Product_follower` ( `ID_user` );

CREATE TABLE trueque.`Comment` ( 
	`ID_product`         INT  NOT NULL  ,
	`ID_sender`          INT  NOT NULL  ,
	`Comment_subject`    VARCHAR( 100 )    ,
	`Comment_text`       TEXT    ,
	`Comment_datetime`   DATETIME  NOT NULL  ,
	CONSTRAINT pk_comment PRIMARY KEY ( `ID_product`, `ID_sender` )
 );

CREATE INDEX ID_sender ON trueque.`Comment` ( `ID_sender` );

CREATE TABLE trueque.`Bid` ( 
	`ID_bid`             INT  NOT NULL  AUTO_INCREMENT,
	`ID_product`         INT  NOT NULL  ,
	`ID_bidder`          INT  NOT NULL  ,
	`BID_Q`              INT    ,
	`BID_ID_product`     INT    ,
	`BID_datetime`       DATETIME  NOT NULL  ,
	CONSTRAINT pk_bid PRIMARY KEY ( `ID_bid` )
 );

CREATE INDEX ID_product ON trueque.`Bid` ( `ID_product` );

CREATE INDEX ID_bidder ON trueque.`Bid` ( `ID_bidder` );

CREATE INDEX BID_ID_product ON trueque.`Bid` ( `BID_ID_product` );

CREATE TABLE trueque.`Message` ( 
	`ID_message`         INT  NOT NULL  AUTO_INCREMENT,
	`ID_conversation`    INT  NOT NULL  ,
	`ID_sender`          INT  NOT NULL  ,
	`ID_receiver`        INT  NOT NULL  ,
	`Message_subject`    VARCHAR( 100 )  NOT NULL  ,
	`Message_text`       TEXT    ,
	`Message_datetime`   DATETIME  NOT NULL  ,
	`Message_read`       BIT  NOT NULL  ,
	CONSTRAINT pk_message PRIMARY KEY ( `ID_message`, `ID_conversation` )
 );

CREATE INDEX ID_sender ON trueque.`Message` ( `ID_sender` );

CREATE INDEX ID_receiver ON trueque.`Message` ( `ID_receiver` );

CREATE TABLE trueque.`Trade` ( 
	`ID_trade`           INT  NOT NULL  AUTO_INCREMENT,
	`ID_dealer`          INT    ,
	`ID_bid`             INT    ,
	`Trade_code_dealer`  VARCHAR( 10 )    ,
	`Trade_code_bidder`  INT    ,
	`Trade_pending_dealer` BIT  NOT NULL  ,
	`Trade_pending_bidder` BIT  NOT NULL  ,
	`Trade_datetime`     DATETIME  NOT NULL  ,
	`Trade_valid`        BIT  NOT NULL  ,
	CONSTRAINT pk_trade PRIMARY KEY ( `ID_trade` )
 );

CREATE INDEX ID_dealer ON trueque.`Trade` ( `ID_dealer` );

CREATE INDEX ID_bid ON trueque.`Trade` ( `ID_bid` );

CREATE TABLE trueque.`Album` ( 
	`ID_album`           INT  NOT NULL  AUTO_INCREMENT,
	`ID_owner`           INT  NOT NULL  ,
	`Album_name`         VARCHAR( 20 )  NOT NULL  ,
	CONSTRAINT pk_album PRIMARY KEY ( `ID_album` )
 );

CREATE INDEX ID_owner ON trueque.`Album` ( `ID_owner` );

CREATE TABLE trueque.`Album_product` ( 
	`ID_album`           INT  NOT NULL  ,
	`ID_product`         INT  NOT NULL  ,
	CONSTRAINT pk_album_product PRIMARY KEY ( `ID_album`, `ID_product` )
 );

CREATE INDEX ID_product ON trueque.`Album_product` ( `ID_product` );

CREATE TABLE trueque.`Invitation` ( 
	`ID_sender`          INT  NOT NULL  ,
	`Invitation_email`   VARCHAR( 30 )  NOT NULL  ,
	`Invitation_token`   VARCHAR( 50 )  NOT NULL  ,
	`Invitation_pending` BIT  NOT NULL  ,
	CONSTRAINT pk_invitation PRIMARY KEY ( `ID_sender`, `Invitation_email` )
 );

CREATE TABLE trueque.`Notification` ( 
	`ID_user`            INT  NOT NULL  ,
	`Notification_datetime` DATETIME  NOT NULL  ,
	`Notification_message` TEXT  NOT NULL  ,
	`Notification_pending` BIT  NOT NULL  ,
	`Notification_link`  VARCHAR( 50 )  NOT NULL  ,
	CONSTRAINT pk_notification PRIMARY KEY ( `ID_user`, `Notification_datetime` )
 );

CREATE TABLE trueque.`Precios` ( 
	`Precio_datetime`    DATETIME  NOT NULL  ,
	`Bajo`               INT  NOT NULL  ,
	`Alto`               INT  NOT NULL  ,
	CONSTRAINT pk_precios PRIMARY KEY ( `Precio_datetime` )
 );

ALTER TABLE trueque.`City` ADD CONSTRAINT `City_ibfk_1` FOREIGN KEY ( `ID_country` ) REFERENCES trueque.`Country`( `ID_country` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE trueque.`Usuario` ADD CONSTRAINT `Usuario_ibfk_1` FOREIGN KEY ( `Usuario_city` ) REFERENCES trueque.`City`( `ID_city` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE trueque.`Rating` ADD CONSTRAINT `Rating_ibfk_1` FOREIGN KEY ( `ID_rater` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE trueque.`Rating` ADD CONSTRAINT `Rating_ibfk_2` FOREIGN KEY ( `ID_rated` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Followers` ADD CONSTRAINT `Followers_ibfk_1` FOREIGN KEY ( `ID_follower` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Followers` ADD CONSTRAINT `Followers_ibfk_2` FOREIGN KEY ( `ID_followed` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Warning` ADD CONSTRAINT `Warning_ibfk_1` FOREIGN KEY ( `ID_sender` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Warning` ADD CONSTRAINT `Warning_ibfk_2` FOREIGN KEY ( `ID_receiver` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Warning` ADD CONSTRAINT `Warning_ibfk_3` FOREIGN KEY ( `Warning_reason` ) REFERENCES trueque.`WarningReason`( `ID_reason` ) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE trueque.`Product` ADD CONSTRAINT `Product_ibfk_1` FOREIGN KEY ( `ID_owner` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Product_category` ADD CONSTRAINT `Product_category_ibfk_1` FOREIGN KEY ( `ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Product_category` ADD CONSTRAINT `Product_category_ibfk_2` FOREIGN KEY ( `ID_category` ) REFERENCES trueque.`Category`( `ID_category` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Product_follower` ADD CONSTRAINT `Product_follower_ibfk_1` FOREIGN KEY ( `ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Product_follower` ADD CONSTRAINT `Product_follower_ibfk_2` FOREIGN KEY ( `ID_user` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Comment` ADD CONSTRAINT `Comment_ibfk_1` FOREIGN KEY ( `ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Comment` ADD CONSTRAINT `Comment_ibfk_2` FOREIGN KEY ( `ID_sender` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Bid` ADD CONSTRAINT `Bid_ibfk_1` FOREIGN KEY ( `ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Bid` ADD CONSTRAINT `Bid_ibfk_2` FOREIGN KEY ( `ID_bidder` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Bid` ADD CONSTRAINT `Bid_ibfk_3` FOREIGN KEY ( `BID_ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Message` ADD CONSTRAINT `Message_ibfk_1` FOREIGN KEY ( `ID_sender` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Message` ADD CONSTRAINT `Message_ibfk_2` FOREIGN KEY ( `ID_receiver` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Trade` ADD CONSTRAINT `Trade_ibfk_1` FOREIGN KEY ( `ID_dealer` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE trueque.`Trade` ADD CONSTRAINT `Trade_ibfk_2` FOREIGN KEY ( `ID_bid` ) REFERENCES trueque.`Bid`( `ID_bid` ) ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE trueque.`Album` ADD CONSTRAINT `Album_ibfk_1` FOREIGN KEY ( `ID_owner` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Album_product` ADD CONSTRAINT `Album_product_ibfk_1` FOREIGN KEY ( `ID_album` ) REFERENCES trueque.`Album`( `ID_album` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Album_product` ADD CONSTRAINT `Album_product_ibfk_2` FOREIGN KEY ( `ID_product` ) REFERENCES trueque.`Product`( `ID_product` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Invitation` ADD CONSTRAINT `Invitation_ibfk_1` FOREIGN KEY ( `ID_sender` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE trueque.`Notification` ADD CONSTRAINT `Notification_ibfk_1` FOREIGN KEY ( `ID_user` ) REFERENCES trueque.`Usuario`( `ID_usuario` ) ON DELETE CASCADE ON UPDATE NO ACTION;

