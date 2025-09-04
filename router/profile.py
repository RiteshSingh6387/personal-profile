# backend/routers/profile.py
from fastapi import APIRouter
from schemas import ProfileCreate  # import the model
from database import get_personal_info_collection  # import the collection function
from fastapi import HTTPException
# create a router instance
router = APIRouter()

@router.post("/create")
def create_profile(profile: ProfileCreate):
    # Get the collection
    try:
        try:
            collection = get_personal_info_collection()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
            
        
        # Insert the profile data into the collection
        try:
            profile_dict = profile.model_dump()
            
            for p in profile_dict["projects"]:
                p["link"] = str(p.get("link", "#"))
            

            collection.insert_one(profile_dict)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create profile: {e}")
        # Return a success message
        return {
            "message": "Profile created successfully",
            "data": profile.model_dump() # return the data we received
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server error: {e}")
        

@router.get("/view")
def get_profile():
    try:

        try:
            collection = get_personal_info_collection()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
            

        try:
            profile = collection.find_one()  # fetch all documents

            # Convert ObjectId → str
            profile["_id"] = str(profile["_id"])

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to fetch profiles: {e}")
            

        return profile
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Internal Server error: {e}")
        


@router.post("/update")
def update_profile(profile: ProfileCreate):
    
    try:
        try:
            collection = get_personal_info_collection()
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Database connection error: {e}")
        
        try:
            profile_dict = profile.model_dump()
            for p in profile_dict["projects"]:
                p["link"] = str(p.get("link", "#"))
            
            result = collection.update_one({}, {"$set": profile_dict})  # Update the first document found

            if result.matched_count == 0:
                raise HTTPException(status_code = 404, detail = f"No profile found to update: {e}")
                

        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Failed to update the profile: {e}")
        

        return {
            "message": "Profile updated successfully",
            "data": profile.model_dump() # return the data we received
        }
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Internal Server error: {e}")