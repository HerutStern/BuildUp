INSERT INTO public.company ("id", "company_name","is_deleted") VALUES
	 (11, 'COMPANY1',false),
	 (6, 'company2',false),
	 (7, 'company3',false),
	 (8, 'company4',false),
	 (9, 'company5',false);

insert into public.auth_user ("id","username","email","password") values
--  (7, 77, null, null, manager1, null, null, 111@gmail.com, null, null, null).
	(7,'manager1','111@gmail.com', '77'),
	(8,'manager2','222@gmail.com', '88'),
	(9,'projectmanager1','333@gmail.com', '99'),
	(10,'projectmanager2','444@gmail.com', '1010'),
	(11,'QUALITY_CHECKER1','555@gmail.com', '1111'),
	(12,'QUALITY_CHECKER1','666@gmail.com', '1212'),
	(13,'PERMIT_INSPECTOR1','777@gmail.com', '1313'),
	(14,'PERMIT_INSPECTOR1','888@gmail.com', '1414'),
	(15, 'FINAL_APPROVAL','999@gmail.com', '1515'),
	(16, 'FINAL_APPROVAL','1010@gmail.com', '1616'),
	(17,'projectmanager1','1717@gmail.com', '1717'),
	(18,'projectmanager1','1818@gmail.com', '1818'),
	(19,'projectmanager1','1919@gmail.com', '1919'),
	(20,'PERMIT_INSPECTOR1','2020@gmail.com', '2020'),
	(21,'PERMIT_INSPECTOR1','2121@gmail.com', '2121'),
	(22,'QUALITY_CHECKER3','2222@gmail.com', '2222'),
	(23,'PERMIT_INSPECTOR5','2323@gmail.com', '2323');


insert into public."permission" ("id","user","company","role") values
	(1,7,11'COMPANY_MANAGER'),
	(2,8,6'COMPANY_MANAGER'),
	(3,9,11,'PROJECT_MANAGER'),
	(4,10,6,'PROJECT_MANAGER'),
	(5,11,11,'QUALITY_CHECKER'),
	(6,12,6,'QUALITY_CHECKER'),
	(7,13,11,'PERMIT_INSPECTOR'),
	(8,14,11,'PERMIT_INSPECTOR'),
	(9,15,11,'FINAL_APPROVAL'),
	(10,16,7,'FINAL_APPROVAL'),
	(11,17,7,'PROJECT_MANAGER'),
	(12,18,8,'PROJECT_MANAGER'),
	(13,19,9,'PROJECT_MANAGER'),
	(14,20,6,'PERMIT_INSPECTOR'),
	(15,21,6,'PERMIT_INSPECTOR'),
	(16,22,7,'QUALITY_CHECKER'),
	(17,23,7,'PERMIT_INSPECTOR'),
	(1,7,7'COMPANY_MANAGER'),
	(2,8,8'COMPANY_MANAGER'),
	(2,8,9'COMPANY_MANAGER');


INSERT INTO public.building_permit ("id","company","project_manager_user_id","building_permit_name") VALUES
	 (1,11,9,'permit1'),
	 (2,6,10,'permit2'),
	 (3,7,17,'permit3'),
	 (4,8,18,'permit4'),
	 (7,9,19,'permit5');

INSERT INTO public.permit_status ("id","building_permit","status","start_date","approving_user_id","is_approved") VALUES
	 (1,1,"EDITING",'2023-01-01',9,true),
	 (2,1,"QUALITY_CHECK",'2023-01-17',11,true),
	 (3,1,"SIGNATURES_ROUND",'2023-01-18',13,true),
	 (4,1,"SIGNATURES_ROUND",'2023-01-18',14,true),
	 (5,1,"FINAL_APPROVAL",'2023-01-22',15,true),
	 (6,1,"APPROVED",'2023-01-23',null,null),
	 (7,2,"EDITING",'2023-02-10',10,true),
	 (8,2,"QUALITY_CHECK",'2023-02-11',12,true),
	 (9,2,"SIGNATURES_ROUND",'2023-02-13',20,true),
	 (10,2,"SIGNATURES_ROUND",'2023-02-13',21,null),
	 (11,3,"EDITING",'2023-02-10',17,true),
	 (12,3,"QUALITY_CHECK",'2023-02-14',22,true),
	 (13,3,"SIGNATURES_ROUND",'2023-02-14',23,false),
	 (14,3,"EDITING",'2023-02-14',17,true),
	 (15,3,"QUALITY_CHECK",'2023-02-17',22,true),
	 (16,3,"SIGNATURES_ROUND",'2023-02-17',23,true),
	 (17,3,"FINAL_APPROVAL",'2023-02-19',16,false),
	 (18,3,"CANCELLED",'2023-02-20',null,null),
	 (19,4,"EDITING",'2023-02-20',null,null),
	 (20,7,"EDITING",'2023-02-21',null,null);

INSERT INTO public.sections_template ("id","company","section_name","is_deleted") VALUES
	 (1,11,'building permit maximum height'),
	 (2,11,'Description'),
	 (3,11,'Depth'),
	 (4,6,'building permit maximum height'),
	 (5,7,'building permit maximum height'),
	 (6,8,'building permit maximum height'),
	 (7,9,'building permit maximum height');

INSERT INTO public.files_template ("id","company","file_name","is_deleted") VALUES
	 (1,11,'drawing'),
	 (2,6,'a signed excavation permit'),
	 (3,6,'signature of the project manager'),
	 (4,6,'drawing'),
	 (5,7,'drawing'),
	 (6,8,'drawing'),
	 (7,9,'drawing');

insert into public.permit_section ("id","sections_template","building_permit","content","is_deleted") values
	(1,1,1,'3.5 m'),
	(2,2,1,'this is a description'),
	(3,3,1,'4.5 m'),
	(4,4,2,'3.6 m'),
	(1,5,3,'3.5 m'),
	(1,6,4,'8 m'),
	(1,7,7,'we do not know yet');

insert into public.permits_file ("id","files_template","building_permit","file_link","is_deleted") values
	(1,1,1,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(2,2,2,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(3,3,2,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(4,4,2,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(1,5,3,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(1,6,4,'permits_file_uploads/buildupS_SAe6LKm.jpg'),
	(1,7,7,'permits_file_uploads/buildupS_SAe6LKm.jpg');




commit;

rollback;