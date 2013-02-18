CREATE TABLE Country(
ID_country INTEGER AUTO_INCREMENT NOT NULL,
Country_name VARCHAR (20) NOT NULL,
PRIMARY KEY (ID_country)
);

CREATE TABLE City(
ID_city INTEGER  NOT NULL,
ID_country INTEGER  NOT NULL,
City_name VARCHAR (20) NOT NULL,
PRIMARY KEY (ID_city),
FOREIGN KEY (ID_country) REFERENCES Country(ID_country)
);

CREATE TABLE Usuario (
ID_usuario INTEGER AUTO_INCREMENT NOT NULL,
Usuario_password VARCHAR (25) NOT NULL,
Usuario_name VARCHAR (20) NOT NULL,
Usuario_lastname VARCHAR (20) NOT NULL,
Usuario_bulletins BOOLEAN NOT NULL,
Usuario_email_1 VARCHAR (30) UNIQUE NOT NULL,
Usuario_email_2 VARCHAR (30) NULL,
Usuario_phone_1 VARCHAR (10) NULL,
Usuario_phone_2 VARCHAR (10) NULL,
Usuario_language VARCHAR (5) NULL,
Usuario_FB_Token VARCHAR (150) NULL,
Usuario_TW_Token VARCHAR (160) NULL,
Usuario_register_date DATETIME  NOT NULL,
Usuario_active BOOLEAN NOT NULL;
Usuario_city INTEGER  NULL,
Usuario_level INTEGER  NOT NULL DEFAULT 0,
Usuario_rating INTEGER  NOT NULL DEFAULT 0,
Usuario_ranking_qty INTEGER  NULL DEFAULT 0,
Usuario_quds INTEGER  NOT NULL DEFAULT 0,
Usuario_follower_qty INTEGER  NOT NULL DEFAULT 0,
Usuario_followed_qty INTEGER  NOT NULL DEFAULT 0,
Usuario_barter_qty INTEGER  NOT NULL DEFAULT 0,
Usuario_remaining_invitations INTEGER  NOT NULL DEFAULT 15,
Usuario_art BOOLEAN  NOT NULL,
Usuario_music BOOLEAN  NOT NULL,
Usuario_tech BOOLEAN  NOT NULL,
Usuario_cars BOOLEAN  NOT NULL,
Usuario_travels BOOLEAN  NOT NULL,
Usuario_clothes BOOLEAN  NOT NULL,
Usuario_cine BOOLEAN  NOT NULL,
Usuario_sports BOOLEAN  NOT NULL,
Usuario_eco BOOLEAN  NOT NULL,
Usuario_culture BOOLEAN  NOT NULL,
Usuario_spectacles BOOLEAN  NOT NULL,
Usuario_love BOOLEAN  NOT NULL,
Usuario_food BOOLEAN  NOT NULL,
Usuario_vacations BOOLEAN  NOT NULL,
Usuario_services BOOLEAN  NOT NULL,
PRIMARY KEY (ID_usuario),
FOREIGN KEY (Usuario_city) REFERENCES City(ID_city)
);

CREATE TABLE Rating(
ID_rating INTEGER AUTO_INCREMENT NOT NULL,
ID_rater INTEGER,
ID_rated INTEGER  NOT NULL,
Rating_level INTEGER  NOT NULL,
Rating_datetime DATETIME  NOT NULL,
PRIMARY KEY (ID_rating),
FOREIGN KEY (ID_rater) REFERENCES Usuario(ID_usuario) ON DELETE SET NULL, 
FOREIGN KEY (ID_rated) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Followers(
ID_follower INTEGER  NOT NULL,
ID_followed INTEGER  NOT NULL,
PRIMARY KEY (ID_follower, ID_followed),
FOREIGN KEY (ID_follower) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE,
FOREIGN KEY (ID_followed) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE WarningReason(
ID_reason INTEGER AUTO_INCREMENT NOT NULL,
Reason_text VARCHAR(50) NOT NULL,
PRIMARY KEY(ID_reason)
);


CREATE TABLE Warning(
ID_warning INTEGER AUTO_INCREMENT NOT NULL,
ID_sender INTEGER  NOT NULL,
ID_receiver INTEGER  NOT NULL,
Warning_reason INTEGER,
Warning_message TEXT  NOT NULL,
Warning_datetime INTEGER  NOT NULL,
PRIMARY KEY (ID_warning),
FOREIGN KEY (ID_sender) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE,
FOREIGN KEY (ID_receiver) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE,
FOREIGN KEY (Warning_reason) REFERENCES WarningReason(ID_reason) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Category(
ID_category INTEGER AUTO_INCREMENT NOT NULL,
Category_name VARCHAR (20) NOT NULL,
PRIMARY KEY (ID_category)
);


CREATE TABLE Product(
ID_product INTEGER AUTO_INCREMENT NOT NULL,
ID_owner INTEGER  NOT NULL,
Product_name VARCHAR (30) NOT NULL,
Product_img VARCHAR  (100) NOT NULL,
Product_description TEXT  NULL,
Product_Q_amount INTEGER  NOT NULL DEFAULT 0,
Product_datetime DATETIME  NOT NULL,
Product_follower_qty INTEGER  NOT NULL DEFAULT 0,
Product_visit_qty INTEGER  NOT NULL DEFAULT 0,
Product_country VARCHAR (20) NOT NULL,
Product_city VARCHAR (20) NOT NULL,
PRIMARY KEY (ID_product),
FOREIGN KEY (ID_owner) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);



CREATE TABLE Product_category(
ID_product INTEGER  NOT NULL,
ID_category INTEGER NOT NULL,
PRIMARY KEY (ID_product, ID_category),
FOREIGN KEY (ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE,
FOREIGN KEY (ID_category) REFERENCES Category(ID_category) ON DELETE CASCADE
);

CREATE TABLE Product_follower(
ID_product INTEGER  NOT NULL,
ID_user INTEGER  NOT NULL,
PRIMARY KEY (ID_product, ID_user),
FOREIGN KEY (ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE,
FOREIGN KEY (ID_user) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Comment(
ID_product INTEGER  NOT NULL,
ID_sender INTEGER  NOT NULL,
Comment_subject VARCHAR(100)  NULL,
Comment_text TEXT  NULL,
Comment_datetime DATETIME  NOT NULL,
PRIMARY KEY (ID_product, ID_sender),
FOREIGN KEY (ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE,
FOREIGN KEY (ID_sender) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Bid(
ID_bid INTEGER AUTO_INCREMENT NOT NULL,
ID_product INTEGER  NOT NULL,
ID_bidder INTEGER  NOT NULL,
BID_Q INTEGER  NULL,
BID_ID_product INTEGER  NULL,
BID_datetime DATETIME  NOT NULL,
CONSTRAINT PK_Bid PRIMARY KEY (ID_bid),
FOREIGN KEY (ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE,
FOREIGN KEY (ID_bidder) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE,
FOREIGN KEY (BID_ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE
);


CREATE TABLE Message(
ID_message INTEGER AUTO_INCREMENT NOT NULL,
ID_conversation INTEGER NOT NULL,
ID_sender INTEGER  NOT NULL,
ID_receiver INTEGER  NOT NULL,
Message_subject VARCHAR(100)  NOT NULL,
Message_text TEXT  NULL,
Message_datetime DATETIME  NOT NULL,
Message_read BOOLEAN  NOT NULL,
PRIMARY KEY (ID_message, ID_conversation),
FOREIGN KEY (ID_sender) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE,
FOREIGN KEY (ID_receiver) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Trade(
ID_trade INTEGER AUTO_INCREMENT NOT NULL,
ID_dealer INTEGER,
ID_bid INTEGER,
Trade_code_dealer VARCHAR (10) NULL,
Trade_code_bidder INTEGER  NULL,
Trade_pending_dealer BOOLEAN  NOT NULL,
Trade_pending_bidder BOOLEAN  NOT NULL,
Trade_datetime DATETIME  NOT NULL,
Trade_valid BOOLEAN  NOT NULL,
PRIMARY KEY (ID_trade),
FOREIGN KEY (ID_dealer) REFERENCES Usuario(ID_usuario) ON DELETE SET NULL,
FOREIGN KEY (ID_bid) REFERENCES Bid(ID_bid) ON DELETE SET NULL 
);

CREATE TABLE Album(
ID_album INTEGER AUTO_INCREMENT NOT NULL,
ID_owner INTEGER  NOT NULL,
Album_name VARCHAR (20) NOT NULL,
Album_edit BOOLEAN  NOT NULL,
PRIMARY KEY (ID_album),
FOREIGN KEY (ID_owner) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);


CREATE TABLE Album_product(
ID_album INTEGER  NOT NULL,
ID_product INTEGER  NOT NULL,
PRIMARY KEY (ID_album, ID_product),
FOREIGN KEY (ID_album) REFERENCES Album(ID_album) ON DELETE CASCADE,
FOREIGN KEY (ID_product) REFERENCES Product(ID_product) ON DELETE CASCADE
);

CREATE TABLE Invitation(
ID_sender INTEGER  NOT NULL,
Invitation_email VARCHAR (30) NOT NULL,
Invitation_token VARCHAR (50) NOT NULL,
Invitation_pending BOOLEAN  NOT NULL,
PRIMARY KEY (ID_sender, Invitation_email),
FOREIGN KEY (ID_sender) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);


CREATE TABLE Notification(
ID_user INTEGER  NOT NULL,
Notification_message TEXT  NOT NULL,
Notification_pending BOOLEAN NOT NULL,
Notification_datetime DATETIME NOT NULL,
Notification_link VARCHAR (50) NOT NULL,
PRIMARY KEY (ID_user, Notification_datetime),
FOREIGN KEY (ID_user) REFERENCES Usuario(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Precios(
Bajo INTEGER  NOT NULL,
Alto INTEGER  NOT NULL,
Precio_datetime DATETIME NOT NULL,
PRIMARY KEY(Precio_datetime)
);

