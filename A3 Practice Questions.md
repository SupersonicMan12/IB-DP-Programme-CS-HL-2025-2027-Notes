## A3.1

> [!IB Style Question] Question 1 — A3.1.1 Features of a relational database
> An online bookshop stores its data in a relational database. Two of its tables are shown below.
>
> **Customer**
>
> | CustomerID | Name        | Email              |
> | ---------- | ----------- | ------------------ |
> | C001       | Hana Sato   | hana@mail.com      |
> | C002       | Tom Reyes   | tom.r@mail.com     |
>
> **Order**
>
> | OrderID | OrderDate  | CustomerID |
> | ------- | ---------- | ---------- |
> | 5001    | 2026-02-11 | C001       |
> | 5002    | 2026-02-12 | C002       |
> | 5003    | 2026-02-15 | C001       |
>
> **(a)** State the term used for a single row in a table. **[1]**
>
> **(b)** Define the term *primary key*. **[1]**
>
> **(c)** Outline how the Customer and Order tables are linked. **[2]**
>
> **(d)** Identify the type of relationship between Customer and Order, and outline why it is this type. **[2]**

a) record
b) primary key is the unique identifier of a record
c) Order uses CustomerID as a foreign key referencing the primary key of Customer, CustomerID
d) Customer : Order = 1 : N, as each order has only one customer and a customer can have multiple orders. 

> [!IB Style Question] Question 2 — A3.1.1 Benefits of a relational database
> A secondary school currently stores student information in separate spreadsheets kept by each department. The administration, science and sports departments each keep their own copy of every student's name, address and emergency contact. The school plans to replace the spreadsheets with a single relational database.
>
> **(a)** Identify **two** benefits of a relational database, other than reduced redundancy. **[2]**
>
> **(b)** Explain how the relational database would reduce data redundancy and improve data consistency compared with the spreadsheets. **[3]**
>
> **(c)** Several teachers may update the same student's record at the same time. Describe how concurrency control helps in this situation. **[2]**
>
> **(d)** Outline **one** security feature a relational database could provide to protect the students' emergency contact details. **[2]**

a) Relational databases are more efficient to query with: SQL allows for logical queries. Relational databases offer better data integrity.
b) 
1. each student's details are stored once, in a single student table
2. other tables refer to the student by a StudentID foreign key instead of copying the details
3. a change is made once and seen everywhere, so there are no conflicting versions
c) concurrency makes it so that there can only be one editor of a record at a time. this is so that each teacher's changes are guaranteed to be saved (no loss or overwriting).
d) User privileges are set so that only administration staff accounts can read the EmergencyContact field. Teachers query the database through a view that leaves this field out, so they can't see it.

> [!IB Style Question] Question 3 — A3.1.1 Relationships
> **(a)** For each of the following pairs of entities, identify the type of relationship (one-to-one, one-to-many or many-to-many). **[3]**
>
> - (i) Country and CapitalCity, where each country has exactly one capital city.
> - (ii) Author and Book, where an author can write many books but each book has exactly one author.
> - (iii) Student and Course, where a student can take many courses and a course has many students.
>
> **(b)** Explain why a many-to-many relationship cannot be implemented directly between two tables, and how it is resolved in a relational database. **[3]**
>
> **(c)** Distinguish between a mandatory relationship and an optional relationship, using the Author and Book example in **(a)(ii)**. **[2]**

a) one-to-one; one-to-many; many-to-many
b) due to atomicity in relational databases, each field can only have one value. a many-to-many relationship means there may be multiple references needed in the same field. a junction table is created to pair each matching, where two foreign keys form a composite primary key.
c) A mandatory relationship means a record must reference or depend on another: a book must have an author (the foreign key is NOT NULL). An optional relationship means a record does not necessarily need another: an author does not have to write books (can be NULL).

> [!IB Style Question] Question 4 — A3.1.1 Limitations of a relational database
> A social media company stores user posts, photographs, short videos and comment threads, where a comment can have replies, which can themselves have replies, to any depth. The platform has over one billion users and receives millions of new posts every hour. The application is written in an object-oriented programming language.
>
> **(a)** Outline what is meant by *object-relational impedance mismatch*. **[2]**
>
> **(b)** Discuss whether a relational database is a suitable choice for storing this company's data. **[6]**

a) 
1. Objects can contain nested objects, lists and inheritance, but relational databases store data as flat tables of rows and columns
2. Extra mapping code (e.g. an ORM) is needed to convert objects to rows and back, which adds complexity and slows development

b) 

AGAINST:
1. Big data scalability: a billion users and millions of posts per hour need horizontal scaling, but relational databases scale vertically
2. Unstructured data: photos and videos don't fit fixed columns and can't be queried meaningfully
3. Hierarchical data: nested replies need a self-referencing FK, so each thread takes recursive queries or many joins, slow
4. Impedance mismatch: OOP application needs mapping code (ORM) to convert objects to and from flat tables
FOR:
5. ACID, integrity and concurrency: user accounts and payments must be accurate and safe when many users update data at once
CONCLUSION:
6. Hybrid: relational for accounts and transactions; NoSQL or object storage for posts, threads and media.

## A3.2

> [!IB Style Question] Question 5 — A3.2.1 Database schemas
> A hospital is designing a new database to manage patients, doctors and appointments.
>
> **(a)** State the schema level at which data types and indexes are specified. **[1]**
>
> **(b)** Distinguish between a conceptual schema and a logical schema. **[2]**
>
> **(c)** Describe **one** benefit of producing a conceptual schema before the physical schema. **[2]**
>
> **(d)** The hospital later moves its database to a different database management system (DBMS). Outline why the physical schema may need to change while the logical schema remains the same. **[2]**

a) Physical schema
b) Conceptual schema identifies the entities and their relationships; logical schema further considers the specific attributes and primary/foreign keys that the conceptual schema does not identify
c) the conceptual schema is more generic and offers a blueprint, catching design errors early when they are cheap to fix; it can also be shown to non-technical stakeholders. The physical schema can then safely build on the conceptual schema by providing the specific implementation details of data types and indices.
d) The logical schema stays the same because the entities, attributes, keys and relationships don't change. Physical schema is DBMS-specific: data type names, storage structures and index types must be redefined to adapt to different systems (MySQL vs Oracle)

> [!IB Style Question] Question 6 — A3.2.2 Entity relationship diagrams
> A veterinary clinic stores data about owners, pets, vets and appointments.
>
> - Each owner registers one or more pets. Each pet belongs to exactly one owner.
> - Each pet may have zero or more appointments. Each appointment is for exactly one pet.
> - Each appointment is with exactly one vet. A vet can have many appointments, but a newly hired vet may have none.
>
> **(a)** Construct an entity relationship diagram (ERD) for this scenario, showing the entities, relationships, cardinality and modality. **[5]**
>
> **(b)** Outline **one** reason an ERD should be produced before the database is implemented. **[2]**
>
> **(c)** Explain how the modality of the relationship between Appointment and Vet affects the foreign key in the Appointment table. **[2]**

a) 

Owner:
OwnerID (PK)

Pet:
PetID (PK)
OwnerID (FK referencing Owner's OwnerID)

Appointment
AppointmentID (PK)
VetID (FK referencing Vet's VetID)
PetID (FK referencing Pet's PetID)

Vet
VetID (PK)
VetStatus

Any FK reference means that it is N:1

b) ERD offers a blueprint of the relationships between entities. It can help identify errors while fixing is cheap. Otherwise, many implementation details would have to be modified

c) Each appointment must have one vet. This is mandatory, that is, the vet field is NOT NULL. A vet, on the other hand, may have no appointments, which is optional

> [!IB Style Question] Question 7 — A3.2.3 Data types
> A gym chain stores the following fields about each member:
>
> | Field          | Example value     | Notes                                       |
> | -------------- | ----------------- | ------------------------------------------- |
> | MemberID       | GM00421           | Always 7 characters                         |
> | JoinDate       | 2025-09-01        |                                             |
> | MonthlyFee     | 29.99             |                                             |
> | MembershipType | Premium           | Only "Basic", "Premium" or "Student"        |
> | PhoneNumber    | 07700 900123      |                                             |
>
> **(a)** State the most appropriate data type for MemberID, JoinDate, MonthlyFee and MembershipType. **[4]**
>
> **(b)** Distinguish between the CHAR and VARCHAR data types. **[2]**
>
> **(c)** A developer stores PhoneNumber using the INT data type. Explain **two** problems this could cause. **[3]**
>
> **(d)** One branch of the gym stores MonthlyFee as VARCHAR, while all other branches store it as a numeric type. Explain why data type consistency is important when head office calculates total monthly income across all branches. **[2]**

a) CHAR(7), DATE, FLOAT, ENUM of ("Basic", "Premium", "Student")
b) CHAR is a string of fixed length, VARCHAR can have variable length
c) Leading zeros are lost. Special formatting like - or + cannot be stored. Overflow may occur.
d) VARCHAR cannot be logically correctly added with a numeric type, which can cause error when the head office tries to calculate. Even to fix, conversions have to be made, reducing speed

> [!IB Style Question] Question 8 — A3.2.4 Constructing tables and keys
> A football club records which players appeared in each match.
>
> **Player**(PlayerID, PlayerName, Position)
>
> **Match**(MatchID, MatchDate, Opponent)
>
> **Appearance**
>
> | PlayerID | MatchID | MinutesPlayed | Goals |
> | -------- | ------- | ------------- | ----- |
> | P07      | M01     | 90            | 1     |
> | P11      | M01     | 64            | 0     |
> | P07      | M02     | 90            | 2     |
> | P04      | M02     | 25            | 0     |
>
> **(a)** Explain why neither PlayerID nor MatchID alone can be the primary key of the Appearance table. **[2]**
>
> **(b)** Identify the foreign key(s) in the Appearance table and the table each one references. **[2]**
>
> **(c)** A designer suggests adding PlayerName to the Appearance table so that reports are easier to produce. Explain why this is poor design. **[2]**
>
> **(d)** Explain how well-defined tables, using primary key and foreign key constraints, help to ensure data integrity in this database. **[3]**

a) MinutesPlayed and Goals depend on both PlayerID and MatchID. A primary key must be able to uniquely determine a record: yet the same player can be in multiple records and the same match can be in multiple records
b) Foreign keys are PlayerID and MatchID: referencing Player(PlayerID) and MatchID(Match)
c) Because the same player can be referenced multiple times, there would be data redundant. The table is also not maximally modular: attributes in the new table depend directly on only part of the primary key
d) Well-defined tables have that each foreign key validly references another table's entry, and that each primary key uniquely identifies a record. DBMS rejects invalid data: an appearance row without a player should indeed not be allowed.

> [!IB Style Question] Question 9 — A3.2.5 Normal forms
> A school stores examination results in the following table, which is in first normal form (1NF). The primary key is the composite key (StudentID, SubjectCode).
>
> **Result**(<u>StudentID</u>, <u>SubjectCode</u>, StudentName, SubjectTeacher, TeacherRoom, Mark)
>
> Each subject is taught by one teacher, and each teacher has one room.
>
> **(a)** Define the term *atomicity* in the context of normalization. **[1]**
>
> **(b)** Identify **one** partial-key dependency in the Result table, and outline why it is a partial-key dependency. **[2]**
>
> **(c)** Identify **one** transitive dependency in the Result table, and outline why it is a transitive dependency. **[2]**
>
> **(d)** State the conditions a table must meet to be in third normal form (3NF). **[2]**
>
> **(e)** Explain why a table that is in 1NF and has a single-attribute primary key is automatically in second normal form (2NF). **[2]**

a) atomicity means that each entry has only one value
b) StudentName only depends on StudentID, not on the composite key of SubjectCode. So it depends partially
c) Teacher Room depends on Subject Teacher, which depends on the combination of StudentID and SubjectCode. So it depends transitively.
d) It must satisfy the three properties of atomicity, no partial dependency and no transitive dependency
e) When only single-attribute primary keys exist, partial dependency cannot exist because no composite keys exist, that is, no attribute can only depend on one of the multiple parts.

> [!IB Style Question] Question 10 — A3.2.6 Normalizing to 3NF
> A music school keeps all of its enrolment data in one unnormalized table. Each course is taught by exactly one tutor, and a tutor may teach several courses. EnrolDate is the date a student enrolled on a particular course.
>
> | StudentID | StudentName | CourseCode | CourseName                     | Fee      | TutorID | TutorName        | TutorEmail             | EnrolDate              |
> | --------- | ----------- | ---------- | ------------------------------ | -------- | ------- | ---------------- | ---------------------- | ---------------------- |
> | 1001      | Mei Tan     | PIA1, GTR2 | Piano Grade 1, Guitar Grade 2  | 300, 250 | T7, T3  | R. Osei, L. Park | osei@ms.org, park@ms.org | 2026-01-10, 2026-01-12 |
> | 1002      | Jonas Berg  | GTR2       | Guitar Grade 2                 | 250      | T3      | L. Park          | park@ms.org            | 2026-01-15             |
> | 1003      | Aisha Khan  | VLN1, PIA1 | Violin Grade 1, Piano Grade 1  | 280, 300 | T7, T7  | R. Osei, R. Osei | osei@ms.org, osei@ms.org | 2026-02-01, 2026-02-03 |
>
> **(a)** Explain why this table is not in first normal form (1NF). **[2]**
>
> **(b)** State a suitable primary key for the table once it has been converted to 1NF. **[1]**
>
> **(c)** Construct a set of tables in third normal form (3NF) for this data. For each table, state the primary key and any foreign keys. **[6]**
>
> **(d)** Explain why EnrolDate must be stored in the same table as the composite key. **[2]**

a) No atomicity: e.g. 1001 CourseCode has two entries, 1001 CourseName has two entries.
b) (StudentID, CourseCode)
c) 

Student:
StudentID (PK)
StudentName

Course:
CourseCode (PK)
CourseName 
Fee
Tutor (FK)

Selection:
CourseCode (FK, PK composite)
StudentID (FK, PK composite)
EnrolDate

Tutor:
TutorID (PK)
Name
Email

d) The Enrolment Date depends on both StudentID and CourseCode. Student 1001 enrolled on PIA1 on 01-10 and GTR2 01-12

> [!IB Style Question] Question 11 — A3.2.5 Normalization issues
> A hospital stores ward allocations in a single table. The primary key is PatientID.
>
> | PatientID | PatientName | WardCode | WardName    | Floor | NurseInCharge |
> | --------- | ----------- | -------- | ----------- | ----- | ------------- |
> | P01       | Leo Grant   | W1       | Cardiology  | 3     | N. Adeyemi    |
> | P02       | Sara Novak  | W2       | Maternity   | 1     | K. Ito        |
> | P03       | Omar Haddad | W1       | Cardiology  | 3     | N. Adeyemi    |
> | P04       | Lina Cruz   | W3       | Paediatrics | 2     | B. Moreau     |
>
> **(a)** Identify **one** transitive dependency in this table, and outline why it is a transitive dependency. **[2]**
>
> **(b)** With reference to the data above, explain how this table leads to data duplication. **[2]**
>
> **(c)** With reference to the data above, explain how this table can lead to missing data. **[2]**
>
> **(d)** Outline how normalizing this table to 3NF would resolve these issues. **[2]**

a) Floor depends on WardName, which depends on PatientID. This is transitive dependency
b) Information about the same ward is repeated across records: W1 Cardiology Floor 3 Nurse N Adeyemi is repeated twice.
c) A ward can't be recorded without a patient. Ward details are lost when the last patient leaves.
d) Ward(WardCode PK, WardName, Floor, NurseInCharge) Patient(PatientID PK, PatientName, WardCode FK). Each ward's detail is stored once, is independent of patients and the transitive dependence is removed.

> [!IB Style Question] Question 12 — A3.2.7 Denormalization
> A news website stores its articles, authors and categories in a database normalized to 3NF. Every time an article page is displayed, the database joins the Article, Author and Category tables. The website receives around 50 million page views per day, but articles are rarely edited after publication.
>
> **(a)** Outline what is meant by *denormalization*. **[2]**
>
> **(b)** Evaluate the decision to denormalize the news website's database. **[6]**

a) Denormalization means deliberately adding redundant data or merging tables, to reduce joins and speed up reads.
b) 
Advantage: 
- Read performance increases, as no more joins are necessary. This is important as there are 50M views per day (2)
- Queries can be simpler. (1)
Disadvantage:
- Updating an article may require updating multiple parts of the denormalized table, time consuming (1)
- Increased storage use: the table becomes larger, mapping all posisble searches with lots of redundancy (1)
Evaluation: Articles are rarely edited, so the inconsistency risk is low and can be handled with checks. The read gain far outweighs the cost, so denormalizing is justified (1)
## A3.3

> [!IB Style Question] Question 13 — A3.3.1 Data language types
> A cinema stores its data in the following two tables. Questions 14 to 16 and 18 also refer to these tables.
>
> **Film**
>
> | FilmID | Title            | Genre  | Duration | Rating |
> | ------ | ---------------- | ------ | -------- | ------ |
> | F01    | The Silent Coast | Drama  | 128      | PG     |
> | F02    | Star Hunters     | Sci-Fi | 142      | 12     |
> | F03    | Laugh Track      | Comedy | 95       | PG     |
> | F04    | Starfall         | Sci-Fi | 117      | 15     |
> | F05    | The Last Orchard | Drama  | 104      | 12     |
>
> **Screening**
>
> | ScreeningID | FilmID | ScreenDate | Screen | TicketsSold |
> | ----------- | ------ | ---------- | ------ | ----------- |
> | S101        | F02    | 2026-03-01 | 1      | 180         |
> | S102        | F01    | 2026-03-01 | 2      | 75          |
> | S103        | F02    | 2026-03-02 | 1      | 210         |
> | S104        | F04    | 2026-03-02 | 3      | 95          |
> | S105        | F03    | 2026-03-03 | 2      | 60          |
> | S106        | F04    | 2026-03-04 | 1      | 130         |
> | S107        | F02    | 2026-03-05 | 2      | 40          |
>
> **(a)** Distinguish between data definition language (DDL) and data manipulation language (DML). **[2]**
>
> **(b)** Classify each of the following SQL commands as DDL or DML: `ALTER`, `SELECT`, `TRUNCATE`, `UPDATE`, `CREATE`, `DELETE`. **[3]**
>
> **(c)** Distinguish between `DROP TABLE Screening` and `TRUNCATE TABLE Screening`. **[2]**
>
> **(d)** Construct the SQL statement to create the Screening table. Your answer should include appropriate data types, a primary key and a foreign key. **[4]**

a) DDL creates the overall framework of the table, specifying columns and references. DML involves queries and changes that change the records.
b) DDL, DML, DDL, DML, DDL, DML
c) DROP TABLE Screening deletes the table altogether; TRUNCATE TABLE Screening removes all entries while still retaining the table itself
d) 
CREATE TABLE Screening(
ScreeningID CHAR(4) PRIMARY KEY NOT NULL,
FilmID CHAR(3) NOT NULL,
ScreenDate DATE,
Screen INT,
TicketsSold INT,
FOREIGN KEY(FilmID) REFERENCES Film(FilmID)
)


> [!IB Style Question] Question 14 — A3.3.2 Constructing queries
> Refer to the Film and Screening tables in Question 13.
>
> **(a)** Construct an SQL query to list the title and duration of all films that are **not** rated "PG" and have a duration between 100 and 130 minutes inclusive, ordered from shortest to longest. **[3]**
>
> **(b)** Construct an SQL query to list the title and screen date of every screening of a Sci-Fi film shown in screen 1 or screen 3, with the most recent screening first. **[4]**
>
> **(c)** Construct an SQL query to list, without duplicates, the titles of all films beginning with "The" that have at least one screening. **[3]**

a) SELECT title, duration FROM Film WHERE Rating <> "PG" AND Duration BETWEEN 100 AND 130 ORDER BY Duration ASC
b) SELECT f.title, s.ScreenDate From Film f JOIN Screening s ON Film.FilmID = Screening.FilmID WHERE (s.Screen = 1 OR s.Screen = 3) AND f.Genre = 'Sci-Fi' ORDER BY ScreenDate DESC
c) ==🔴SELECT DISTINCT s.Title FROM Film f JOIN Screening s ON Film.FilmID = Screening.FilmID GROUP BY s.Title HAVING s.Title LIKE "The%" AND COUNT(\*) >= 1==

SELECT DISTINCT f.Title FROM Film f JOIN Screening s ON f.FilmID = s.FilmID WHERE f.Title LIKE 'The%'

> [!IB Style Question] Question 15 — A3.3.2 Query output and errors
> Refer to the Film and Screening tables in Question 13.
>
> **(a)** Determine the output of the following query. **[3]**
>
> ```sql
> SELECT DISTINCT f.Title, f.Duration
> FROM Film f
> JOIN Screening s ON f.FilmID = s.FilmID
> WHERE f.Title LIKE 'Star%' AND s.TicketsSold > 100
> ORDER BY f.Duration DESC;
> ```
>
> A student writes the following query, intending to list each film title alongside the tickets sold for its screenings:
>
> ```sql
> SELECT Title, TicketsSold
> FROM Film, Screening
> WHERE TicketsSold > 100;
> ```
>
> **(b)** State the number of rows returned by the student's query, and explain why the result is incorrect. **[3]**
>
> **(c)** The student corrects the query, but adds `FilmID` to the `SELECT` clause without a table name. Outline why the DBMS reports an error. **[2]**

a) 
Star Hunters, 142
Starfall 117

b) a cartesian product is obtained, where every record from Film is paired with every record from Screening. This gives 5 times 3 = 15 rows returned. This is incorrect because it ignores the relationship that links the two tables: Film.FilmID = Screen.FilmID, and allows an instance playing a certain movie to pair with another movie.

c) DBMS would not know which table the FilmID refers to; it is ambiguous. Although it is present in both tables, it is conventional and required that the table name is specified when multiple tables are involved.

> [!IB Style Question] Question 16 — A3.3.3 Updating data
> Refer to the Film and Screening tables in Question 13. The FilmID column in Screening is a foreign key referencing Film.
>
> **(a)** Construct an SQL statement to add a new screening, S108, of film F05 on 2026-03-06 in screen 2, with no tickets sold yet. **[2]**
>
> **(b)** A further 25 tickets have been sold for screening S105. Construct an SQL statement to update the record. **[2]**
>
> **(c)** A member of staff wants to remove screening S107, but runs the statement `DELETE FROM Screening;`. Outline the consequence of this statement and write the correct statement. **[2]**
>
> **(d)** Explain why the statement `DELETE FROM Film WHERE FilmID = 'F02';` may be rejected by the DBMS. **[2]**

a) INSERT INTO Screening (ScreeningID, FilmID, ScreenDate, Screen, TicketsSold) VALUES ("S108", "F05", "2026-03-06", 2, 0)
b) UPDATE Screening SET TicketsSold = TicketsSold + 25 WHERE ScreeningID = "S105"
c) DELETE FROM Screening misses the WHERE keyword, which specifies the exact entries that are deleted. Missing that condition by default deletes all the rows, meaning all the records are los. The correct statement appends WHERE ScreeningID = "S107"
d) If another table's foreign key references this record, DBMS may reject the statement. This is to ensure consistency, so that every foreign key references something real.

> [!IB Style Question] Question 17 — A3.3.3 Indexes and performance
> A national cinema chain's Screening table now contains 40 million rows. Indexes have been created on the FilmID, ScreenDate and TicketsSold columns. TicketsSold is updated every time a ticket is sold.
>
> **(a)** Outline the purpose of an index in a database. **[2]**
>
> **(b)** Explain why the index on TicketsSold may reduce the overall performance of the database. **[3]**
>
> **(c)** At the end of the year, 30 million old screening records are deleted. Describe why the indexes may need to be rebuilt or reorganized after this operation. **[3]**

a) An index is a lookup structure that makes SELECT faster. It creates a quick mapping between the required data and the exact location of the information
b) Indices may negative affect overall performance:
- every INSERT/UPDATE/DELETE on an indexed column must also update the corresponding index, thus writing overall becomes slower. Every time a ticket is sold, this takes a toll on speed
- if the cinema wants to make bulk changes, the indices may become fragmented, which would require a rebuild or reorganization
c) The deleted entries are scattered through the index. This causes fragmentation so lookups get slower. Rebuild can drop the index and recreate it compactly, while reorganize can defragment it in place.

> [!IB Style Question] Question 18 — A3.3.4 Aggregate functions (HL only)
> Refer to the Film and Screening tables in Question 13.
>
> **(a)** Determine the output of the following query. **[3]**
>
> ```sql
> SELECT f.Genre, SUM(s.TicketsSold) AS Total, COUNT(*) AS Shows
> FROM Film f
> JOIN Screening s ON f.FilmID = s.FilmID
> GROUP BY f.Genre
> HAVING SUM(s.TicketsSold) > 70
> ORDER BY Total DESC;
> ```
>
> **(b)** Construct an SQL query to display the title of each film and its average number of tickets sold per screening, only for films whose average is greater than 100, with the highest average first. **[4]**
>
> **(c)** Distinguish between the `WHERE` clause and the `HAVING` clause. **[2]**
>
> **(d)** Construct an SQL query to find the highest number of tickets sold in a single screening of a Drama film. **[2]**

a) Shows:
Sci-Fi, 655, 5
Drama, 75, 1

b) SELECT f.Title, AVERAGE(s.TicketsSold) FROM Film f JOIN Screening s ON Film.FilmID = Screening.FilmID GROUP BY f.Title HAVING AVERAGE(s.TicketsSold) > 100 ORDER BY AVERAGE(s.TicketsSold) DESC

c) WHERE is a by-record filter that occurs before HAVING. HAVING is applied after groups are created, and are evaluated by group.

d) SELECT MAX(s.TicketsSold) FROM Film f JOIN Screening s ON Film.FilmID = Screening.FilmID WHERE f.Genre = 'Drama'

> [!IB Style Question] Question 19 — A3.3.5 Database views (HL only)
> The cinema chain's head office wants a daily sales report. Part-time staff at each cinema should be able to see screening times and ticket sales, but not the financial data stored in other tables.
>
> **(a)** Distinguish between a virtual view and a materialized (snapshot) view. **[2]**
>
> **(b)** Construct an SQL statement to create a view named `DailySales` that shows each screen date and the total number of tickets sold on that date. **[3]**
>
> **(c)** Outline **one** reason why `DailySales` cannot be used to update the underlying Screening table. **[2]**
>
> **(d)** Outline how a view can be used to improve security for the part-time staff. **[2]**
>
> **(e)** Head office runs a monthly report that aggregates all 40 million screening records. Explain **one** advantage and **one** disadvantage of using a materialized view for this report. **[4]**

a) a virtual view is temporarily assembled by joining different tables and presenting it to a user. A materialized view is stored as a table copy and is stored permanently rather than temporarily.
b) CREATE VIEW DailySales AS SELECT ScreenDate, SUM(TicketsSold) FROM Screening GROUP BY ScreenDate
c) DdailySales uses SUM / GROUP BY, so each row of the view is a summary of many Screening rows. If someone changed the total for 2026-03-01 to 300, the DBMS can't tell which instance changed or by how much.
d) The view shows only the information needed for the part-time job. Staff are given access to the views only, not to the underlying tables.
e) One advantage is the report is permanently stored. This means that whenever the administrator wants to read the report again, computation can be saved because the view no longer has to be created from the original table again. One disadvantage is the storage space needed for the materialized view: the materialized view is a stored result of processing the underlying database.

> [!IB Style Question] Question 20 — A3.3.6 Transactions (HL only)
> A concert-ticketing website books a seat and records the payment using the following SQL:
>
> ```sql
> BEGIN TRANSACTION;
> UPDATE Seat SET Status = 'Booked', CustomerID = 'C381' WHERE SeatID = 'A12' AND EventID = 'E09';
> INSERT INTO Payment (PaymentID, CustomerID, EventID, Amount) VALUES ('PY7731', 'C381', 'E09', 85.00);
> COMMIT;
> ```
>
> **(a)** Define the term *transaction*. **[1]**
>
> **(b)** Describe the role of `BEGIN TRANSACTION`, `COMMIT` and `ROLLBACK` in this booking. **[3]**
>
> **(c)** Explain how atomicity and durability ensure the booking is processed reliably. **[4]**
>
> **(d)** Two customers attempt to book seat A12 for event E09 at the same moment. Explain how isolation prevents the seat from being sold twice. **[3]**

a) transaction is a set of SQL statements treated as a single block.
b) BEGIN TRANSACTION signifies the beginning of a transaction; COMMIT means applying all the changing in the TRANSACTION to the database, as a final confirmation; ROLLBACK is automatically applied when an error occurs during ANY ONE of the the SQL statements, reverting the changes of all the previous SQL statements and returning the DB to its status quo.
c) Atomicity states that each transaction is atomic. This means that either all changes are applied or no changes are applied. This is important to ensure that the booking is consistent: e.g. the seat UPDATE succeeds but the payment INSERT fails. 
Durability means that once committed, the change is saved, being able to survive a crash or power loss. This means that once COMMIT is run, the user's booking data is not prone to loss.
d) Isolation means that concurrent transactions do not see each other's half-finished work. This means that if customer A books the seat first, customer B would only see seat booked due to the completely finished work of A. Without isolation, both transactions could read A12 as available before either writes; with isolation, A's transaction locks the seat row, and B must wait until A commits.

## My Grading Report

**Total: 133/183 (73%)**, first attempts only, all 20 questions attempted

| Q   | Topic                         | Score |
| --- | ----------------------------- | ----- |
| 1   | A3.1.1 Features               | 6/6   |
| 2   | A3.1.1 Benefits               | 6/9   |
| 3   | A3.1.1 Relationships          | 7/8   |
| 4   | A3.1.1 Limitations            | 3/8   |
| 5   | A3.2.1 Schemas                | 5/7   |
| 6   | A3.2.2 ERDs                   | 6/9   |
| 7   | A3.2.3 Data types             | 10/11 |
| 8   | A3.2.4 Tables and keys        | 7/9   |
| 9   | A3.2.5 Normal forms           | 8/9   |
| 10  | A3.2.6 Normalizing to 3NF     | 7/11  |
| 11  | A3.2.5 Normalization issues   | 5/8   |
| 12  | A3.2.7 Denormalization        | 3/8   |
| 13  | A3.3.1 DDL / DML              | 8/11  |
| 14  | A3.3.2 Constructing queries   | 7/10  |
| 15  | A3.3.2 Query output / errors  | 6/8   |
| 16  | A3.3.3 Updating data          | 6/8   |
| 17  | A3.3.3 Indexes                | 6/8   |
| 18  | A3.3.4 Aggregates (HL)        | 10/11 |
| 19  | A3.3.5 Views (HL)             | 8/13  |
| 20  | A3.3.6 Transactions (HL)      | 9/11  |

| Section                       | Score | %   |
| ----------------------------- | ----- | --- |
| A3.1 (Q1–4)                   | 22/31 | 71% |
| A3.2.1–3 (Q5–7)               | 21/27 | 78% |
| A3.2.4–7 (Q8–12)              | 30/45 | 67% |
| A3.3 SQL and updates (Q13–17) | 33/45 | 73% |
| A3.3 HL (Q18–20)              | 27/35 | 77% |

**Recurring mistakes**
1. **Not using the scenario trigger** (Q2d, Q4b, Q5d, Q12b, Q14b, Q17b, Q20c, Q20d): definitions correct, application mark lost. Ask "why is this sentence in the stem?"
2. **SQL precision** (~6 marks): quote strings/dates in `'single quotes'`, use the alias everywhere once set (`f.FilmID`, not `Film.FilmID`), don't drop `SELECT`, no `SHORT` type.
3. **Concept gaps**: modality (min, NOT NULL) vs cardinality (max, 1:N); a view is a **saved query**, not a copy, unless materialized.
4. **6-mark discuss / evaluate** (Q4b 3/6, Q12b 2/6): lowest-scoring question type. Structure: for (2, scenario-linked) → against (2, scenario-linked) → weigh against scenario → justified conclusion.

**Other lost marks**
- Vague definitions (Q4a impedance mismatch)
- Query tracing: apply DISTINCT, read values from the table (Q15a)
- Write all selected columns in traced output (Q18a)
- 3NF construction (Q10c): attributes placed in the wrong table / dropped. Use the "depends on what?" test, then tick off every original column
- Normalization issues (Q11c–d): missing data = facts about one entity only exist inside another's rows (ward lost when last patient leaves). Test: would 3NF fix it?
- Denormalization (Q12): purpose = fewer joins → faster reads; ALWAYS say read-intensive. "Evaluate" = weigh each point against the scenario (50M views, rarely edited), then a justified conclusion. Misread "views" as "edits"

**Strongest:** data types (Q7 10/11), normal-form theory (Q9 8/9), aggregates (Q18 10/11)
**Weakest:** A3.2.4–7 application (67%): theory is solid, marks lost applying it to a specific table/scenario

**Next steps**
1. Practise A3.2.6 normalization on the other scenarios in A3.2 notes (library, hospital, inventory…), using the "depends on what?" test
2. Before every answer, underline the numbers / specific phrases in the stem and make sure each appears in the answer
3. Write one timed 6-mark discuss/evaluate answer per week using the for → against → weigh → conclude structure

