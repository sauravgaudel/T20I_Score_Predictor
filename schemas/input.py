from pydantic import BaseModel, computed_field, Field, model_validator
from typing import Annotated

class Input(BaseModel):

    batting_team: Annotated[str, Field(...)]
    bowling_team: Annotated[str, Field(...)]
    current_score: Annotated[int, Field(..., ge=0)]
    overs : Annotated[float, Field(..., gt=0, lt=20)]
    wicket_fall: Annotated[int, Field(..., ge=0, le=10)]
    last_five: Annotated[int, Field(..., ge=0)]

    @model_validator(mode='after')
    def validate_last_five(self):
        if self.last_five> self.current_score:
            raise ValueError('Last 5 over run cannot be greater than current run')
        return self
    
    @model_validator(mode="after")
    def validate_over(self):
        whole = int(self.overs)
        balls = round((self.overs - whole) * 10)

        if whole<5:
            raise ValueError("Over should be greater than five")
        
        if balls < 0 or balls > 5:
            raise ValueError("Invalid overs format. Balls must be between 0 and 5")
        return self
    
    @model_validator(mode="after")
    def validate_teams(self):
        if self.batting_team == self.bowling_team:
            raise ValueError("Batting team and bowling team cannot be the same")
        return self
    
    @computed_field
    @property
    def balls_left(self) -> int:
        return 120 - (int(self.overs)*6 + int((self.overs - int(self.overs))*10))
    
    @computed_field
    @property
    def wicket_left(self) -> int:
        return 10 - self.wicket_fall
    
    @computed_field
    @property
    def CRR(self) -> float:
        return self.current_score / self.overs
    