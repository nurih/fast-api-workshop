from enum import Enum
import pathlib
import statistics as stats
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

api = FastAPI()


class MarklarLevel(Enum):
    '''
    The Marklar Level
    
    Marklar Levels go from `one` to `three` and denote marklar.
    '''
    One = 'one'
    Two = 'two'
    Three = 'three'


class ReviewSummary(BaseModel):
    subject: str = Field(title='Rated Item',
                         alias='RatedItem', max_length=24, min_length=2)
    stars: float = Field(title='Average Review', alias='AverageReview',
                         description='The mathematical mean across all reviews for this **RatedItem**')
    review_count: int = Field(
        title='Number of Reviews', alias='NumberOfReviews')


class Review(BaseModel):
    subject: str = Field(default="Bob's Diner")
    author: str = Field(title="The reviewer")
    stars: int = Field(gt=0, le=5, alias="rating")
    marklar_level: MarklarLevel = Field(default=MarklarLevel.One)


reviews = []


@api.get("/reviews/{subject}", response_model=ReviewSummary)
async def get(subject: str):
    stars = [r.stars for r in reviews if r.subject == subject]
    if len(stars):
        return ReviewSummary(subject=subject, review_count=len(reviews), stars=stats.mean(stars))

    raise HTTPException(status.HTTP_404_NOT_FOUND)


@api.post("/reviews", status_code=status.HTTP_201_CREATED)
async def create_review(review: Review):
    reviews.append(review)
    return {'ok': review}


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api", reload=True)
