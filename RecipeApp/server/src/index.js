import express from "express"; //E of Mern creates API
import cors from "cors"; // communication front end and back end
import mongoose from "mongoose"; // database management system 

import { userRouter } from './routes/users.js';
import { recipesRouter } from './routes/recipes.js';

const app = express();

app.use(express.json());
app.use(cors());

app.use("/auth", userRouter);
app.use("/recipes", recipesRouter);



mongoose.connect(
    "mongodb+srv://lucassotomayor:pookiebear@recipes.odi7bhx.mongodb.net/recipes?retryWrites=true&w=majority", 
    {
    useNewUrlParser:true,
    useUnifiedTopology: true,
    }   
)

app.listen(3001, () => console.log("Server Started"));
