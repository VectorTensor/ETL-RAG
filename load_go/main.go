package main

import (
	"fmt"
	"os"
  "encoding/csv"

	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	_ "gorm.io/driver/postgres"
)

type dbData  struct{

  product_id int  
  customer_id int
  cogs float32
  quantity int
  unit_sale_price float32

 
}



func  InsertData[T any](data T,db *gorm.DB) *gorm.DB {

  res := db.Create(&data)

  return res

}

func main(){

  _ = godotenv.Load()
  host:=os.Getenv("host")
  user:=os.Getenv("user")
  password:=os.Getenv("password")
  dbname:=os.Getenv("dbname")


  fmt.Println("connecting")
  // connStr := "postgres://prat:party%40me@localhost:5432/dummydb?sslmode=disable"
  // dsn := "host=localhost user=prat password=party@me dbname=dummydb sslmode=disable"
  dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=disable", host, user,password, dbname)

  db, _ :=  gorm.Open(postgres.Open(dsn),&gorm.Config{})

  fmt.Println("opened")
  // if err != nil{
  //
  //   fmt.Println("Sorry some error occured !!")

  fmt.Println("connected")
  _ = db.AutoMigrate(&dbData{})

  data := dbData{Name:"Prats",Email:"mnchad@Me"}

  res := InsertData(data,db)

  fmt.Println(res)

}
  





