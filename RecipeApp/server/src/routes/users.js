import express from "express";
import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
import { UserModel } from "../models/Users.js";


const router = express.Router();

router.post("/register", async (req, res) => {
    const {username, password} = req.body;

    const user = await UserModel.findOne({username});

    if(user){
        return res.json({message: "User already exist!"});
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = new UserModel({username, password: hashedPassword});
    await newUser.save();

    res.json({message: "User Registed Successfully!"});
})


 
router.post("/login", async (req, res)=> {
    const {username, password} = req.body;
    const user = await UserModel.findOne({username});

    if(!user){
        return res.json({message: "User doesnt exist!"});
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);

    if(isPasswordValid){
        res.json({message: "username or password is incorrect!"});
    }

    const token = jwt.sign({id: user._id}, "secret");
    res.json({token, userID: user._id});
});

export{router as userRouter};

export const verifyToken = (req, res, next) => {
    const token = req.headers.authorization;

    if(token) {
        jwt.verify(token, "secret", (err) => {
            if (err) return res.sendstatus(403);
            next();


        })
    } else {
        res.sendstatus(401);
    }


}