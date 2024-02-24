import {useEffect} from 'react'
import { useState } from 'react'
import { useGetUserId } from '../hooks/useGetUserId'
import axios  from 'axios';


export const SavedRecipes = () => {
    const userID = useGetUserId();
    const [savedRecipes, setSavedRecipes] = useState([]);
    

    useEffect(() => {
       
        const fetchSavedRecipes = async () => {
            try{
                  const response = await axios.get(`http://localhost:3001/recipes/savedRecipes/${userID}`);
                  setSavedRecipes(response.data.savedRecipes);
               }catch (err){
                       console.error(err);
                   }
                  
               }
               fetchSavedRecipes();
    },  []);

    console.log(savedRecipes);
  return (
    <div>
      <h1>Saved Recipes</h1>
      <ul>
        {savedRecipes.map((recipe) => (
          <li key={recipe._id}>
            <div>
              <h2>{recipe.name}</h2>
            </div>
            <div className='instructions'>
              <p>{recipe.instructions}</p>
            </div>
            <p>{recipe.description}</p>
            <img src={recipe.imageUrl} alt={recipe.name} />
            <p>Cooking Time: {recipe.cookingTime} minutes</p>
          </li>
        ))}
      </ul>
    </div>
  )


}