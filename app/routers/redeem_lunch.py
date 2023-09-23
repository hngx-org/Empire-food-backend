from fastapi import FastAPI, HTTPException, Depends, status
from app.schemas.redeem_lunch import RedeemRequest
from app.models.lunch import RedeemLunch  # Import your Lunch model
from sqlalchemy.orm import Session
from app.db.database import get_db


app = FastAPI()



@app.post("api/user/redeem", response_model=dict)
async def redeem_lunch(redeem_request: RedeemRequest, db: Session = Depends(get_db)):
    try:
        for lunch_id in redeem_request.ids :
            lunch = db.query(RedeemLunch).filter(RedeemLunch.id == lunch_id).first()


            if lunch:
                if not lunch.redeem:
                    lunch.redeem = True
                    db.commit()
                else: 
                    raise HTTPException(status_code=400,
                                        detail=f"Lunch credit with ID {lunch_id} has already been redeemed")
            
            else :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail=f"Lunch credit with ID {lunch_id} not found")

        # Commit to DB
        db.commit()

        return{
            "message":"success",
            "statusCode": 200,
            "data":None
        }

    except Exception as e :
        # Handle exception here
        db.rollback()
        raise HTTPException(status_code=500,detail="An error occured while redeeming lunch credits")
    finally:
        db.close()
    
